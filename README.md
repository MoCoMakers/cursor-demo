# Investment Portfolio Web Application - A Demo of using Cursor.
Relevant prompts are [available here](https://docs.google.com/document/d/1xWvUv9rvVbaR-K3LWZX0Ax7ltBbBfaBMt-i-QGTXDAg/edit?usp=sharing)

A modern web application for managing investment portfolios, built with Flask, Apache, and MySQL in a Docker environment.

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design for portfolio management
- **AI-Powered Trading**: Bayesian investment strategies using PyMC3 and machine learning
- **Paper Trading**: Risk-free trading simulation using Alpaca API
- **Database Integration**: MySQL backend for data persistence
- **Docker Environment**: Easy setup and deployment with Docker Compose
- **Apache Web Server**: Production-ready web server configuration

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- [Git](https://git-scm.com/downloads) (for version control)

## 🛠️ Setup Instructions

### Quick Start (3 steps)

```bash
# 1. Copy environment file
cp env.example .env

# 2. Build and start the application
docker-compose up -d --build

# 3. Access the application
# Web App: http://localhost:8080
# phpMyAdmin: http://localhost:8081
```

### Detailed Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd curor-demo
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

**Quick Setup (Optional):** If you want to use default settings, you can skip editing the `.env` file for now. The application will work with the default values.

Edit the `.env` file with your preferred configuration:

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=investment_portfolio
MYSQL_USER=portfolio_user
MYSQL_PASSWORD=your_password

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=5000

# Alpaca API Configuration (for paper trading)
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### 3. Build and Start the Application

```bash
# Build the Docker images
docker-compose build

# Start all services
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

### 4. Access the Application

Once the containers are running, you can access the application at:

- **Web Application**: http://localhost:8080
- **Database**: localhost:3306 (MySQL)

### 5. Database Setup

The database will be automatically created on first run. If you need to reset the database:

```bash
# Stop the application
docker-compose down

# Remove the database volume
docker volume rm curor-demo_mysql_data

# Restart the application
docker-compose up -d
```

## 🏗️ Project Structure

```
curor-demo/
├── app/                    # Flask application
│   ├── __init__.py        # Flask app initialization
│   ├── routes.py          # Application routes
│   ├── models.py          # Database models
│   ├── bayesian_service.py # AI trading service
│   ├── static/            # Static files (CSS, JS, images)
│   └── templates/         # HTML templates
│       ├── index.html     # Main landing page
│       ├── dashboard.html # Portfolio dashboard
│       └── trading.html   # AI trading dashboard
├── docker/                # Docker configuration files
│   ├── apache/           # Apache configuration
│   └── mysql/            # MySQL configuration
├── docker-compose.yml     # Docker Compose configuration
├── docker-compose.dev.yml # Development overrides
├── docker-compose.prod.yml # Production overrides
├── Dockerfile             # Flask application Dockerfile
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
└── README.md             # This file
```

## 🐳 Docker Services

The application runs the following services:

- **web**: Apache web server with mod_wsgi for Flask
- **app**: Flask application container
- **db**: MySQL database server
- **phpmyadmin**: Database management interface (optional)

### Docker Compose Configurations

The project includes three Docker Compose files:

- **`docker-compose.yml`**: Base configuration with all services
- **`docker-compose.dev.yml`**: Development overrides (hot reload, additional ports)
- **`docker-compose.prod.yml`**: Production overrides (Gunicorn, resource limits, security)

## 🔧 Development

### Running in Development Mode

```bash
# Start with development settings (includes hot reload and additional ports)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Or start with basic configuration
docker-compose up -d
```

### Viewing Logs

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f app
docker-compose logs -f db
```

### Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (database data)
docker-compose down -v

# Stop development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

## 🧠 Key Concepts and Classes

### Core Architecture

The application follows a **Model-View-Controller (MVC)** pattern with the following key components:

#### Database Models (`app/models.py`)
- **`Portfolio`**: Represents investment portfolios with relationships to investments and trading strategies
- **`Investment`**: Individual investment holdings with symbol, quantity, and purchase price
- **`TradingStrategy`**: AI trading strategies with statistical parameters (alpha, beta, sigma)
- **`Trade`**: Individual paper trades with prediction data and performance metrics
- **`MarketData`**: Historical price data for analysis and backtesting

#### AI Trading Service (`app/bayesian_service.py`)
- **`BayesianTradingService`**: Core service implementing statistical trading strategies
  - **Market Data Integration**: Fetches real-time data from Alpaca API using `alpaca-py`
  - **Statistical Analysis**: Uses `scipy.stats.linregress` for return prediction
  - **Signal Generation**: Creates buy/sell signals based on predicted returns
  - **Paper Trading**: Executes simulated trades with position sizing and risk management

#### Web Interface (`app/templates/`)
- **`index.html`**: Main landing page with navigation to trading dashboard
- **`dashboard.html`**: Portfolio management interface
- **`trading.html`**: AI trading dashboard with strategy creation and monitoring

### Statistical Trading Algorithm

The AI trading system uses a **linear regression model** for return prediction:

1. **Data Collection**: Fetches historical price data from Alpaca API
2. **Return Calculation**: Computes daily returns from price data
3. **Model Fitting**: Fits linear regression to identify trends
4. **Prediction**: Predicts next day's return using fitted model
5. **Signal Generation**: Creates buy/sell signals based on predictions and confidence thresholds

### API Integration

- **Alpaca API (`alpaca-py`)**: Modern Python SDK for market data and paper trading
- **Trading Client**: Handles order execution and account management
- **Data Client**: Retrieves historical market data for analysis

## 🤖 AI Trading Features

### Statistical Investment Strategies

The application includes AI-powered trading strategies using statistical analysis:

- **Statistical Model Fitting**: Linear regression analysis for return prediction
- **Paper Trading**: Risk-free trading simulation using Alpaca API
- **Real-time Analysis**: Live market data analysis and prediction
- **Strategy Management**: Create, configure, and monitor trading strategies

### Getting Started with AI Trading

1. **Access the Trading Dashboard**: Navigate to `/trading` in the web application
2. **Create Sample Data**: Click "Create Sample Data" to populate the database with test data
3. **Create a Strategy**: Set up a new trading strategy with your preferred parameters
4. **Configure Alpaca API**: Add your Alpaca API credentials to the `.env` file for paper trading
5. **Run Analysis**: Use the "Analyze" feature to see predictions without executing trades
6. **Execute Trades**: Run strategies to execute paper trades based on AI predictions

### Alpaca API Setup

To enable paper trading functionality:

1. Sign up for a free Alpaca account at [alpaca.markets](https://alpaca.markets)
2. Get your API key and secret from the Alpaca dashboard
3. Add them to your `.env` file:
   ```env
   ALPACA_API_KEY=your_api_key_here
   ALPACA_SECRET_KEY=your_secret_key_here
   ALPACA_BASE_URL=https://paper-api.alpaca.markets
   ```

### Trading Strategy Components

- **Market Data Analysis**: Historical price data analysis using Alpaca API
- **Statistical Model Fitting**: Linear regression models for return prediction
- **Signal Generation**: Buy/sell signals based on predicted returns
- **Risk Management**: Position sizing and confidence thresholds
- **Performance Tracking**: Win rate and P&L monitoring

## 📊 Viewing Sample Portfolio

### Quick Start - View Sample Data

1. **Start the Application**:
   ```bash
   docker-compose up -d
   ```

2. **Access the Web Interface**:
   - Open your browser and go to: http://localhost:8080
   - You'll see the main landing page for "Investment Portfolio"

3. **Navigate to Trading Dashboard**:
   - Click the "AI Trading Dashboard" button or go to: http://localhost:8080/trading
   - This will take you to the AI trading interface

4. **Create Sample Data**:
   - In the trading dashboard, click the **"Create Sample Data"** button
   - This will populate the database with:
     - Sample portfolio with $100,000 initial value
     - Sample investments (AAPL, GOOGL, MSFT)
     - Sample trading strategies
     - Sample market data for analysis

5. **Explore the Sample Portfolio**:
   - **Portfolio Overview**: View total value, investments, and performance
   - **Trading Strategies**: See sample strategies with different parameters
   - **Recent Trades**: View simulated trades with predictions and outcomes
   - **Market Data**: Access historical price data for analysis

### Sample Data Structure

When you create sample data, the system generates:

- **Portfolio**: "Sample Portfolio" with $100,000 initial value
- **Investments**: 
  - AAPL: 50 shares at $150.00
  - GOOGL: 30 shares at $2,800.00
  - MSFT: 40 shares at $300.00
- **Trading Strategies**:
  - "Conservative AAPL Strategy" (confidence: 0.1, position size: 0.05)
  - "Aggressive GOOGL Strategy" (confidence: 0.05, position size: 0.1)
- **Market Data**: 100 days of historical price data for each symbol

### Using the Sample Data

1. **Analyze Strategies**: Click "Analyze" on any strategy to see predictions
2. **Run Strategies**: Click "Run Strategy" to execute paper trades
3. **View Results**: Check the "Recent Trades" section to see trade outcomes
4. **Monitor Performance**: Track win rates and P&L for each strategy

### Database Access

You can also view the sample data directly in the database:

```bash
# Access phpMyAdmin
# Open: http://localhost:8081
# Username: portfolio_user
# Password: your_password (from .env file)

# Or connect via command line
docker-compose exec db mysql -u portfolio_user -p investment_portfolio
```

## 🗄️ Database Management

### Accessing MySQL

```bash
# Connect to MySQL container
docker-compose exec db mysql -u root -p

# Or use the provided credentials
docker-compose exec db mysql -u portfolio_user -p investment_portfolio
```

### Database Backup

```bash
# Create a backup
docker-compose exec db mysqldump -u root -p investment_portfolio > backup.sql

# Restore from backup
docker-compose exec -T db mysql -u root -p investment_portfolio < backup.sql
```

## 🚀 Deployment

### Production Deployment

1. Update the `.env` file with production settings
2. Set `FLASK_ENV=production` and `FLASK_DEBUG=0`
3. Use a production-ready secret key
4. Configure proper database passwords

```bash
# Production build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or build and start in one command
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**: Change the port mappings in `docker-compose.yml`
2. **Database Connection Issues**: Check the `.env` file configuration
3. **Permission Errors**: Ensure Docker has proper permissions
4. **Apache/Web Server Issues**: 
   - Check if port 8080 is available
   - Verify Apache configuration with `docker-compose logs web`
   - Ensure the Flask app is running before Apache starts

### Useful Commands

```bash
# Rebuild containers
docker-compose build --no-cache

# Restart specific service
docker-compose restart app

# Check container status
docker-compose ps

# Access container shell
docker-compose exec app bash

# View specific service logs
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f web

# Clean up everything (containers, volumes, networks)
docker-compose down -v --remove-orphans
docker system prune -f
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the Docker and Flask documentation
3. Create an issue in the repository

---

**Happy Coding! 🎉** 
