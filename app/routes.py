from flask import Blueprint, render_template, jsonify, request
from app.models import Portfolio, Investment, TradingStrategy, Trade, MarketData
from app.bayesian_service import BayesianTradingService
from app import db
from datetime import datetime
import logging
import numpy as np
from datetime import timedelta

logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main greeting page for the Investment Portfolio application."""
    return render_template('index.html')

@main.route('/health')
def health_check():
    """Health check endpoint for Docker."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'investment-portfolio-api'
    })

@main.route('/api/portfolios')
def get_portfolios():
    """API endpoint to get all portfolios."""
    try:
        portfolios = Portfolio.query.all()
        return jsonify({
            'success': True,
            'portfolios': [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'created_at': p.created_at.isoformat(),
                    'total_value': p.calculate_total_value()
                } for p in portfolios
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/portfolios', methods=['POST'])
def create_portfolio():
    """API endpoint to create a new portfolio."""
    try:
        data = request.get_json()
        portfolio = Portfolio(
            name=data.get('name'),
            description=data.get('description', '')
        )
        db.session.add(portfolio)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'portfolio': {
                'id': portfolio.id,
                'name': portfolio.name,
                'description': portfolio.description,
                'created_at': portfolio.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/dashboard')
def dashboard():
    """Dashboard page showing portfolio overview."""
    portfolios = Portfolio.query.all()
    return render_template('dashboard.html', portfolios=portfolios)

# New routes for Bayesian trading

@main.route('/api/strategies')
def get_strategies():
    """API endpoint to get all trading strategies."""
    try:
        strategies = TradingStrategy.query.all()
        return jsonify({
            'success': True,
            'strategies': [strategy.to_dict() for strategy in strategies]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/strategies', methods=['POST'])
def create_strategy():
    """API endpoint to create a new trading strategy."""
    try:
        data = request.get_json()
        strategy = TradingStrategy(
            name=data.get('name'),
            description=data.get('description', ''),
            symbol=data.get('symbol'),
            confidence_threshold=data.get('confidence_threshold', 0.6),
            position_size=data.get('position_size', 0.1),
            max_position_size=data.get('max_position_size', 0.2),
            portfolio_id=data.get('portfolio_id')
        )
        db.session.add(strategy)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'strategy': strategy.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/strategies/<int:strategy_id>/run', methods=['POST'])
def run_strategy(strategy_id):
    """API endpoint to run a trading strategy."""
    try:
        trading_service = BayesianTradingService()
        result = trading_service.run_strategy(strategy_id)
        
        if result is None:
            return jsonify({
                'success': False,
                'error': 'Strategy not found or inactive'
            }), 404
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logger.error(f"Error running strategy: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/strategies/<int:strategy_id>/analyze', methods=['POST'])
def analyze_strategy(strategy_id):
    """API endpoint to analyze a trading strategy with mockup chart data."""
    try:
        strategy = TradingStrategy.query.get(strategy_id)
        if not strategy:
            return jsonify({
                'success': False,
                'error': 'Strategy not found'
            }), 404
        
        # Generate mockup market data and analysis
        mock_data = generate_mock_market_data(strategy.symbol)
        
        return jsonify({
            'success': True,
            'strategy': strategy.to_dict(),
            'market_data': mock_data['market_data'],
            'returns_data': mock_data['returns_data'],
            'analysis': mock_data['analysis']
        })
    except Exception as e:
        logger.error(f"Error analyzing strategy: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_mock_market_data(symbol):
    """Generate mockup market data and analysis for chart display."""
    import numpy as np
    from datetime import datetime, timedelta
    
    # Generate 100 days of mock market data
    days = 100
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, 0, -1)]
    
    # Generate realistic price movements
    np.random.seed(42)  # For reproducible results
    start_price = 150.0 if symbol == 'AAPL' else 300.0 if symbol == 'MSFT' else 2800.0
    
    prices = [start_price]
    for i in range(1, days):
        # Daily return with some trend and volatility
        daily_return = np.random.normal(0.001, 0.02)  # Small positive trend with volatility
        new_price = prices[-1] * (1 + daily_return)
        prices.append(new_price)
    
    # Generate OHLC data
    market_data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        volatility = price * 0.02
        open_price = price + np.random.normal(0, volatility * 0.5)
        high_price = max(open_price, price) + abs(np.random.normal(0, volatility * 0.3))
        low_price = min(open_price, price) - abs(np.random.normal(0, volatility * 0.3))
        close_price = price
        volume = int(np.random.uniform(1000000, 5000000))
        
        market_data.append({
            'date': date,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
    
    # Calculate returns
    returns = []
    for i in range(1, len(prices)):
        daily_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append({
            'date': dates[i],
            'return': round(daily_return * 100, 2)  # Convert to percentage
        })
    
    # Generate analysis summary
    avg_return = np.mean([r['return'] for r in returns])
    volatility = np.std([r['return'] for r in returns])
    trend = np.polyfit(range(len(returns)), [r['return'] for r in returns], 1)[0]
    
    # Generate trading signal based on recent trend
    recent_returns = [r['return'] for r in returns[-10:]]
    recent_avg = np.mean(recent_returns)
    recent_vol = np.std(recent_returns)
    
    if recent_avg > 0.5 and recent_vol < 2.0:
        action = 'buy'
        reasoning = f'Positive trend detected (avg: {recent_avg:.2f}%) with low volatility ({recent_vol:.2f}%)'
    elif recent_avg < -0.5 and recent_vol < 2.0:
        action = 'sell'
        reasoning = f'Negative trend detected (avg: {recent_avg:.2f}%) with low volatility ({recent_vol:.2f}%)'
    else:
        action = 'hold'
        reasoning = f'Mixed signals - avg return: {recent_avg:.2f}%, volatility: {recent_vol:.2f}%'
    
    analysis = {
        'action': action,
        'reasoning': reasoning,
        'predicted_return': round(recent_avg, 4),
        'confidence': round(1 - recent_vol / 5, 4),  # Higher confidence with lower volatility
        'avg_return': round(avg_return, 2),
        'volatility': round(volatility, 2),
        'trend': round(trend, 4)
    }
    
    return {
        'market_data': market_data,
        'returns_data': returns,
        'analysis': analysis
    }

@main.route('/api/trades')
def get_trades():
    """API endpoint to get all trades."""
    try:
        trades = Trade.query.order_by(Trade.timestamp.desc()).limit(100).all()
        return jsonify({
            'success': True,
            'trades': [trade.to_dict() for trade in trades]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    """API endpoint to get market data for a symbol."""
    try:
        market_data = MarketData.query.filter_by(symbol=symbol).order_by(MarketData.date.desc()).limit(30).all()
        return jsonify({
            'success': True,
            'symbol': symbol,
            'data': [md.to_dict() for md in market_data]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/trading')
def trading_dashboard():
    """Trading dashboard page."""
    strategies = TradingStrategy.query.all()
    trades = Trade.query.order_by(Trade.timestamp.desc()).limit(20).all()
    return render_template('trading.html', strategies=strategies, trades=trades)

@main.route('/api/sample-data', methods=['POST'])
def create_sample_data():
    """API endpoint to create sample data for testing."""
    try:
        # Create sample portfolio
        portfolio = Portfolio(
            name="AI Trading Portfolio",
            description="Portfolio for testing Bayesian trading strategies"
        )
        db.session.add(portfolio)
        db.session.commit()
        
        # Create sample trading strategies
        aapl_strategy = TradingStrategy(
            name="AAPL Statistical Strategy",
            description="Statistical analysis strategy for Apple stock",
            symbol="AAPL",
            confidence_threshold=0.5,
            position_size=0.1,
            max_position_size=0.2,
            portfolio_id=portfolio.id
        )
        db.session.add(aapl_strategy)
        
        msft_strategy = TradingStrategy(
            name="MSFT Statistical Strategy",
            description="Statistical analysis strategy for Microsoft stock",
            symbol="MSFT",
            confidence_threshold=0.6,
            position_size=0.15,
            max_position_size=0.25,
            portfolio_id=portfolio.id
        )
        db.session.add(msft_strategy)
        db.session.commit()
        
        # Create sample market data
        np.random.seed(42)
        days = 100
        dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
        
        # AAPL data
        start_price = 150.0
        prices = [start_price]
        for i in range(1, days):
            change = np.random.normal(0.001, 0.02)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        for i, (date, price) in enumerate(zip(dates, prices)):
            daily_volatility = price * 0.02
            open_price = price + np.random.normal(0, daily_volatility * 0.5)
            high_price = max(open_price, price) + abs(np.random.normal(0, daily_volatility * 0.3))
            low_price = min(open_price, price) - abs(np.random.normal(0, daily_volatility * 0.3))
            close_price = price
            volume = int(np.random.uniform(1000000, 5000000))
            
            market_data = MarketData(
                symbol="AAPL",
                date=date.date(),
                open_price=round(open_price, 2),
                high_price=round(high_price, 2),
                low_price=round(low_price, 2),
                close_price=round(close_price, 2),
                volume=volume
            )
            db.session.add(market_data)
        
        # MSFT data
        start_price = 300.0
        prices = [start_price]
        for i in range(1, days):
            change = np.random.normal(0.0015, 0.025)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        for i, (date, price) in enumerate(zip(dates, prices)):
            daily_volatility = price * 0.025
            open_price = price + np.random.normal(0, daily_volatility * 0.5)
            high_price = max(open_price, price) + abs(np.random.normal(0, daily_volatility * 0.3))
            low_price = min(open_price, price) - abs(np.random.normal(0, daily_volatility * 0.3))
            close_price = price
            volume = int(np.random.uniform(2000000, 6000000))
            
            market_data = MarketData(
                symbol="MSFT",
                date=date.date(),
                open_price=round(open_price, 2),
                high_price=round(high_price, 2),
                low_price=round(low_price, 2),
                close_price=round(close_price, 2),
                volume=volume
            )
            db.session.add(market_data)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sample data created successfully',
            'portfolio_id': portfolio.id,
            'strategies_created': 2,
            'market_data_days': days
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 