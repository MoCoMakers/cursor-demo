#!/usr/bin/env python3
"""
Sample data population script for the Investment Portfolio application.
This script creates sample portfolios, strategies, and market data for testing.
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.insert(0, '/app')

from app import create_app, db
from app.models import Portfolio, Investment, TradingStrategy, MarketData

def create_sample_data():
    """Create sample data for testing."""
    app = create_app()
    
    with app.app_context():
        # Create sample portfolio
        portfolio = Portfolio(
            name="AI Trading Portfolio",
            description="Portfolio for testing Bayesian trading strategies"
        )
        db.session.add(portfolio)
        db.session.commit()
        
        print(f"Created portfolio: {portfolio.name} (ID: {portfolio.id})")
        
        # Create sample trading strategy
        strategy = TradingStrategy(
            name="AAPL Statistical Strategy",
            description="Statistical analysis strategy for Apple stock",
            symbol="AAPL",
            confidence_threshold=0.5,
            position_size=0.1,
            max_position_size=0.2,
            portfolio_id=portfolio.id
        )
        db.session.add(strategy)
        db.session.commit()
        
        print(f"Created strategy: {strategy.name} (ID: {strategy.id})")
        
        # Create sample market data for AAPL
        print("Creating sample market data for AAPL...")
        
        # Generate realistic price data
        np.random.seed(42)
        start_price = 150.0
        days = 100
        dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
        
        prices = [start_price]
        for i in range(1, days):
            # Random walk with slight upward trend
            change = np.random.normal(0.001, 0.02)  # Small positive drift
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        # Create market data records
        for i, (date, price) in enumerate(zip(dates, prices)):
            # Generate OHLC data
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
        
        # Create sample market data for MSFT
        print("Creating sample market data for MSFT...")
        
        start_price = 300.0
        prices = [start_price]
        for i in range(1, days):
            change = np.random.normal(0.0015, 0.025)  # Slightly higher drift
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
        print("Sample data created successfully!")
        print(f"Created {days} days of market data for AAPL and MSFT")
        
        # Create a second strategy for MSFT
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
        
        print(f"Created strategy: {msft_strategy.name} (ID: {msft_strategy.id})")
        
        print("\nSample data summary:")
        print(f"- Portfolio: {portfolio.name}")
        print(f"- Strategies: {strategy.name}, {msft_strategy.name}")
        print(f"- Market data: AAPL ({days} days), MSFT ({days} days)")
        print("\nYou can now test the trading system at http://localhost:8080/trading")

if __name__ == "__main__":
    create_sample_data() 