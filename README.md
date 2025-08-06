# Investment Portfolio Web Application

A modern web application for managing investment portfolios, built with Flask, Apache, and MySQL in a Docker environment.

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design for portfolio management
- **Database Integration**: MySQL backend for data persistence
- **Docker Environment**: Easy setup and deployment with Docker Compose
- **Apache Web Server**: Production-ready web server configuration

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- [Git](https://git-scm.com/downloads) (for version control)

## 🛠️ Setup Instructions

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
```

### 3. Build and Start the Application

#### Option 1: Using Makefile (Recommended)
```bash
# Quick setup (creates .env file, builds, and starts development environment)
make setup

# Or step by step:
make build
make dev
```

#### Option 2: Using Docker Compose directly
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
│   ├── static/            # Static files (CSS, JS, images)
│   └── templates/         # HTML templates
├── docker/                # Docker configuration files
│   ├── apache/           # Apache configuration
│   └── mysql/            # MySQL configuration
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Flask application Dockerfile
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🐳 Docker Services

The application runs the following services:

- **web**: Apache web server with mod_wsgi for Flask
- **app**: Flask application container
- **db**: MySQL database server
- **phpmyadmin**: Database management interface (optional)

## 🔧 Development

### Using the Makefile

The project includes a Makefile with convenient commands for common tasks:

```bash
# View all available commands
make help

# Quick setup (creates .env, builds, and starts dev environment)
make setup

# Development commands
make dev      # Start development environment
make build    # Build Docker images
make up       # Start all services
make down     # Stop all services
make restart  # Restart all services
make logs     # View service logs

# Production commands
make prod     # Start production environment

# Maintenance commands
make clean    # Clean up containers and volumes
make test     # Run tests
```

### Running in Development Mode

```bash
# Start with development settings
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
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
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**: Change the port mappings in `docker-compose.yml`
2. **Database Connection Issues**: Check the `.env` file configuration
3. **Permission Errors**: Ensure Docker has proper permissions

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