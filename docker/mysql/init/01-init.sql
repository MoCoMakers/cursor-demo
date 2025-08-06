-- Investment Portfolio Database Initialization
-- This script runs when the MySQL container starts for the first time

USE investment_portfolio;

-- Create tables if they don't exist (Flask-SQLAlchemy will handle this, but we can add custom indexes)
-- The actual table creation is handled by Flask-SQLAlchemy models

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_portfolio_name ON portfolio(name);
CREATE INDEX IF NOT EXISTS idx_investment_symbol ON investment(symbol);
CREATE INDEX IF NOT EXISTS idx_investment_portfolio_id ON investment(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_investment_purchase_date ON investment(purchase_date);

-- Insert sample data for testing (optional)
INSERT IGNORE INTO portfolio (id, name, description, created_at, updated_at) VALUES
(1, 'Retirement Portfolio', 'Long-term retirement investment strategy', NOW(), NOW()),
(2, 'Growth Portfolio', 'Aggressive growth-focused investments', NOW(), NOW()),
(3, 'Conservative Portfolio', 'Low-risk, stable income investments', NOW(), NOW());

-- Insert sample investments
INSERT IGNORE INTO investment (id, symbol, name, quantity, purchase_price, purchase_date, current_price, current_value, portfolio_id, created_at, updated_at) VALUES
(1, 'AAPL', 'Apple Inc.', 10.0, 150.00, '2023-01-15', 175.00, 1750.00, 1, NOW(), NOW()),
(2, 'GOOGL', 'Alphabet Inc.', 5.0, 2800.00, '2023-02-20', 3200.00, 16000.00, 1, NOW(), NOW()),
(3, 'MSFT', 'Microsoft Corporation', 8.0, 300.00, '2023-03-10', 350.00, 2800.00, 2, NOW(), NOW()),
(4, 'TSLA', 'Tesla Inc.', 15.0, 200.00, '2023-04-05', 250.00, 3750.00, 2, NOW(), NOW()),
(5, 'JNJ', 'Johnson & Johnson', 20.0, 160.00, '2023-05-12', 165.00, 3300.00, 3, NOW(), NOW());

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON investment_portfolio.* TO 'portfolio_user'@'%';
FLUSH PRIVILEGES; 