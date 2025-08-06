-- Investment Portfolio Database Initialization
-- This script runs when the MySQL container starts for the first time

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS investment_portfolio;
USE investment_portfolio;

-- Grant necessary permissions to the application user
GRANT ALL PRIVILEGES ON investment_portfolio.* TO 'portfolio_user'@'%';
FLUSH PRIVILEGES;

-- Note: Tables will be created by Flask-SQLAlchemy when the application starts
-- Sample data can be added through the application or manually after tables are created 