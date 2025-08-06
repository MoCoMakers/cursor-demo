from app import db
from datetime import datetime

class Portfolio(db.Model):
    """Portfolio model for managing investment portfolios."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with investments
    investments = db.relationship('Investment', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    
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