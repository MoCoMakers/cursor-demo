from app import db
from datetime import datetime
import json

class Portfolio(db.Model):
    """Portfolio model for managing investment portfolios."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with investments
    investments = db.relationship('Investment', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    # Relationship with trading strategies
    strategies = db.relationship('TradingStrategy', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total_value(self):
        """Calculate the total value of all investments in the portfolio."""
        return sum(investment.current_value for investment in self.investments)
    
    def to_dict(self):
        """Convert portfolio to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'total_value': self.calculate_total_value(),
            'investment_count': len(self.investments)
        }
    
    def __repr__(self):
        return f'<Portfolio {self.name}>'

class Investment(db.Model):
    """Investment model for individual investments within portfolios."""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    current_price = db.Column(db.Float, default=0.0)
    current_value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to portfolio
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    
    def calculate_gain_loss(self):
        """Calculate the gain/loss for this investment."""
        return self.current_value - (self.quantity * self.purchase_price)
    
    def calculate_gain_loss_percentage(self):
        """Calculate the gain/loss percentage for this investment."""
        if self.quantity * self.purchase_price == 0:
            return 0
        return ((self.current_value - (self.quantity * self.purchase_price)) / 
                (self.quantity * self.purchase_price)) * 100
    
    def update_current_value(self, new_price):
        """Update the current price and value."""
        self.current_price = new_price
        self.current_value = self.quantity * new_price
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert investment to dictionary."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'quantity': self.quantity,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat(),
            'current_price': self.current_price,
            'current_value': self.current_value,
            'gain_loss': self.calculate_gain_loss(),
            'gain_loss_percentage': self.calculate_gain_loss_percentage(),
            'portfolio_id': self.portfolio_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Investment {self.symbol} - {self.name}>'

class TradingStrategy(db.Model):
    """Trading strategy model for Bayesian investment strategies."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    symbol = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Bayesian model parameters (stored as JSON)
    alpha_mean = db.Column(db.Float, default=0.0)
    alpha_std = db.Column(db.Float, default=1.0)
    beta_mean = db.Column(db.Float, default=0.0)
    beta_std = db.Column(db.Float, default=1.0)
    sigma_mean = db.Column(db.Float, default=1.0)
    
    # Trading parameters
    confidence_threshold = db.Column(db.Float, default=0.6)
    position_size = db.Column(db.Float, default=0.1)  # Percentage of portfolio
    max_position_size = db.Column(db.Float, default=0.2)
    
    # Performance tracking
    total_trades = db.Column(db.Integer, default=0)
    winning_trades = db.Column(db.Integer, default=0)
    total_pnl = db.Column(db.Float, default=0.0)
    
    # Foreign key to portfolio
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    
    # Relationship with trades
    trades = db.relationship('Trade', backref='strategy', lazy=True, cascade='all, delete-orphan')
    
    def calculate_win_rate(self):
        """Calculate the win rate of the strategy."""
        if self.total_trades == 0:
            return 0.0
        return (self.winning_trades / self.total_trades) * 100
    
    def to_dict(self):
        """Convert strategy to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symbol': self.symbol,
            'is_active': self.is_active,
            'alpha_mean': self.alpha_mean,
            'beta_mean': self.beta_mean,
            'sigma_mean': self.sigma_mean,
            'confidence_threshold': self.confidence_threshold,
            'position_size': self.position_size,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'win_rate': self.calculate_win_rate(),
            'total_pnl': self.total_pnl,
            'portfolio_id': self.portfolio_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<TradingStrategy {self.name} - {self.symbol}>'

class Trade(db.Model):
    """Trade model for tracking individual trades."""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(4), nullable=False)  # 'buy' or 'sell'
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, filled, cancelled
    pnl = db.Column(db.Float, default=0.0)
    
    # Bayesian prediction data
    predicted_return = db.Column(db.Float)
    confidence = db.Column(db.Float)
    alpha_sample = db.Column(db.Float)
    beta_sample = db.Column(db.Float)
    
    # Foreign keys
    strategy_id = db.Column(db.Integer, db.ForeignKey('trading_strategy.id'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    
    def to_dict(self):
        """Convert trade to dictionary."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'pnl': self.pnl,
            'predicted_return': self.predicted_return,
            'confidence': self.confidence,
            'strategy_id': self.strategy_id,
            'portfolio_id': self.portfolio_id
        }
    
    def __repr__(self):
        return f'<Trade {self.symbol} {self.side} {self.quantity}@{self.price}>'

class MarketData(db.Model):
    """Market data model for storing historical price data."""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert market data to dictionary."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'date': self.date.isoformat(),
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'close_price': self.close_price,
            'volume': self.volume,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<MarketData {self.symbol} {self.date}>' 