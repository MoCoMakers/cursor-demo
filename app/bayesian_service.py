import numpy as np
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from datetime import datetime, timedelta
import logging
from app.models import MarketData, TradingStrategy, Trade
from app import db
import os
from scipy import stats

logger = logging.getLogger(__name__)

class BayesianTradingService:
    """Service for implementing statistical trading strategies."""
    
    def __init__(self, alpaca_api_key=None, alpaca_secret_key=None, alpaca_base_url=None):
        """Initialize the trading service."""
        self.alpaca_api_key = alpaca_api_key or os.getenv('ALPACA_API_KEY')
        self.alpaca_secret_key = alpaca_secret_key or os.getenv('ALPACA_SECRET_KEY')
        self.alpaca_base_url = alpaca_base_url or os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
        
        if self.alpaca_api_key and self.alpaca_secret_key:
            # Initialize new alpaca-py clients
            self.trading_client = TradingClient(
                api_key=self.alpaca_api_key,
                secret_key=self.alpaca_secret_key,
                paper=True
            )
            self.data_client = StockHistoricalDataClient(
                api_key=self.alpaca_api_key,
                secret_key=self.alpaca_secret_key
            )
        else:
            self.trading_client = None
            self.data_client = None
            logger.warning("Alpaca API credentials not provided. Paper trading will be simulated.")
    
    def get_market_data(self, symbol, days=100):
        """Get historical market data from Alpaca API or database."""
        try:
            if self.data_client:
                # Get data from Alpaca API using new alpaca-py
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                request_params = StockBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=TimeFrame.Day,
                    start=start_date,
                    end=end_date
                )
                
                bars = self.data_client.get_stock_bars(request_params)
                
                # Convert to DataFrame
                if bars and hasattr(bars, 'df'):
                    bars_df = bars.df
                else:
                    # Handle single symbol case
                    bars_df = pd.DataFrame([{
                        'open': bar.open,
                        'high': bar.high,
                        'low': bar.low,
                        'close': bar.close,
                        'volume': bar.volume
                    } for bar in bars])
                
                # Store in database
                for index, row in bars_df.iterrows():
                    market_data = MarketData(
                        symbol=symbol,
                        date=index.date() if hasattr(index, 'date') else index,
                        open_price=row['open'],
                        high_price=row['high'],
                        low_price=row['low'],
                        close_price=row['close'],
                        volume=row['volume']
                    )
                    db.session.add(market_data)
                
                db.session.commit()
                return bars_df
            else:
                # Get data from database
                market_data = MarketData.query.filter_by(symbol=symbol).order_by(MarketData.date.desc()).limit(days).all()
                if not market_data:
                    logger.error(f"No market data found for symbol {symbol}")
                    return None
                
                # Convert to DataFrame
                data = []
                for md in reversed(market_data):
                    data.append({
                        'open': md.open_price,
                        'high': md.high_price,
                        'low': md.low_price,
                        'close': md.close_price,
                        'volume': md.volume
                    })
                
                return pd.DataFrame(data)
                
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {str(e)}")
            return None
    
    def calculate_returns(self, price_data):
        """Calculate returns from price data."""
        if price_data is None or len(price_data) < 2:
            return None
        
        prices = price_data['close'].values
        returns = np.diff(prices)
        return returns
    
    def fit_statistical_model(self, returns, strategy_id=None):
        """Fit a simple statistical model to returns data."""
        try:
            if len(returns) < 10:
                return None
            
            # Calculate basic statistics
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            
            # Simple linear trend analysis
            X = np.arange(len(returns))
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, returns)
            
            # Update strategy parameters if provided
            if strategy_id:
                strategy = TradingStrategy.query.get(strategy_id)
                if strategy:
                    strategy.alpha_mean = float(intercept)
                    strategy.alpha_std = float(std_err)
                    strategy.beta_mean = float(slope)
                    strategy.beta_std = float(std_err)
                    strategy.sigma_mean = float(std_return)
                    db.session.commit()
            
            return {
                'intercept': intercept,
                'slope': slope,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err,
                'mean_return': mean_return,
                'std_return': std_return
            }
            
        except Exception as e:
            logger.error(f"Error fitting statistical model: {str(e)}")
            return None
    
    def predict_next_return(self, model_params, next_day_index):
        """Predict the next day's return using the fitted model."""
        try:
            if model_params is None:
                return None, None
            
            # Simple linear prediction
            predicted_return = model_params['intercept'] + model_params['slope'] * next_day_index
            confidence = model_params['std_return']  # Use standard deviation as confidence measure
            
            return predicted_return, confidence
            
        except Exception as e:
            logger.error(f"Error predicting next return: {str(e)}")
            return None, None
    
    def generate_trading_signal(self, strategy, symbol):
        """Generate trading signal based on statistical prediction."""
        try:
            # Get market data
            market_data = self.get_market_data(symbol, days=100)
            if market_data is None:
                return None
            
            # Calculate returns
            returns = self.calculate_returns(market_data)
            if returns is None:
                return None
            
            # Fit statistical model
            model_params = self.fit_statistical_model(returns, strategy.id)
            if model_params is None:
                return None
            
            # Predict next return
            next_day = len(returns)
            predicted_return, confidence = self.predict_next_return(model_params, next_day)
            
            if predicted_return is None:
                return None
            
            # Generate signal based on prediction and confidence
            signal = {
                'symbol': symbol,
                'predicted_return': predicted_return,
                'confidence': confidence,
                'action': 'hold',
                'reasoning': ''
            }
            
            # Simple trading logic
            if predicted_return > 0 and confidence < strategy.confidence_threshold:
                signal['action'] = 'buy'
                signal['reasoning'] = f'Positive return predicted ({predicted_return:.4f}) with acceptable confidence ({confidence:.4f})'
            elif predicted_return < 0 and confidence < strategy.confidence_threshold:
                signal['action'] = 'sell'
                signal['reasoning'] = f'Negative return predicted ({predicted_return:.4f}) with acceptable confidence ({confidence:.4f})'
            else:
                signal['reasoning'] = f'Predicted return ({predicted_return:.4f}) outside confidence threshold ({strategy.confidence_threshold})'
            
            return signal
            
        except Exception as e:
            logger.error(f"Error generating trading signal: {str(e)}")
            return None
    
    def execute_paper_trade(self, strategy, signal):
        """Execute a paper trade based on the signal."""
        try:
            if not signal or signal['action'] == 'hold':
                return None
            
            # Get current price
            if self.trading_client:
                try:
                    # Get latest trade price as approximation for current price
                    latest_trade = self.trading_client.get_latest_trade(signal['symbol'])
                    current_price = latest_trade.price
                except Exception as e:
                    logger.warning(f"Could not get latest trade for {signal['symbol']}: {str(e)}")
                    # Fallback to database price
                    market_data = MarketData.query.filter_by(symbol=signal['symbol']).order_by(MarketData.date.desc()).first()
                    current_price = market_data.close_price if market_data else 100.0
            else:
                # Simulate current price
                market_data = MarketData.query.filter_by(symbol=signal['symbol']).order_by(MarketData.date.desc()).first()
                current_price = market_data.close_price if market_data else 100.0
            
            # Calculate position size
            portfolio = strategy.portfolio
            portfolio_value = portfolio.calculate_total_value()
            position_value = portfolio_value * strategy.position_size
            quantity = position_value / current_price
            
            # Create trade record
            trade = Trade(
                symbol=signal['symbol'],
                side=signal['action'],
                quantity=quantity,
                price=current_price,
                status='filled',
                predicted_return=signal['predicted_return'],
                confidence=signal['confidence'],
                alpha_sample=0.0,  # Could store actual samples
                beta_sample=0.0,
                strategy_id=strategy.id,
                portfolio_id=portfolio.id
            )
            
            db.session.add(trade)
            db.session.commit()
            
            # Update strategy statistics
            strategy.total_trades += 1
            if signal['action'] == 'buy' and signal['predicted_return'] > 0:
                strategy.winning_trades += 1
            elif signal['action'] == 'sell' and signal['predicted_return'] < 0:
                strategy.winning_trades += 1
            
            db.session.commit()
            
            logger.info(f"Executed {signal['action']} trade for {signal['symbol']}: {quantity} shares at ${current_price}")
            return trade
            
        except Exception as e:
            logger.error(f"Error executing paper trade: {str(e)}")
            return None
    
    def run_strategy(self, strategy_id):
        """Run a complete trading strategy."""
        try:
            strategy = TradingStrategy.query.get(strategy_id)
            if not strategy or not strategy.is_active:
                return None
            
            # Generate trading signal
            signal = self.generate_trading_signal(strategy, strategy.symbol)
            if signal is None:
                return None
            
            # Execute trade if signal is not 'hold'
            if signal['action'] != 'hold':
                trade = self.execute_paper_trade(strategy, signal)
                return {
                    'signal': signal,
                    'trade': trade.to_dict() if trade else None
                }
            
            return {'signal': signal, 'trade': None}
            
        except Exception as e:
            logger.error(f"Error running strategy {strategy_id}: {str(e)}")
            return None 