.PHONY: help build up down restart logs clean dev prod test

# Default target
help:
	@echo "Investment Portfolio - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev      - Start development environment"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - View service logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod     - Start production environment"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make test     - Run tests"
	@echo ""

# Development environment
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "Development environment started!"
	@echo "Web Application: http://localhost:8080"
	@echo "Flask Dev Server: http://localhost:5000"
	@echo "phpMyAdmin: http://localhost:8081"

# Production environment
prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "Production environment started!"
	@echo "Web Application: http://localhost:8080"

# Build images
build:
	@echo "Building Docker images..."
	docker-compose build --no-cache
	@echo "Build complete!"

# Start services
up:
	@echo "Starting services..."
	docker-compose up -d
	@echo "Services started!"

# Stop services
down:
	@echo "Stopping services..."
	docker-compose down
	@echo "Services stopped!"

# Restart services
restart:
	@echo "Restarting services..."
	docker-compose restart
	@echo "Services restarted!"

# View logs
logs:
	@echo "Viewing service logs..."
	docker-compose logs -f

# Clean up
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f
	@echo "Cleanup complete!"

# Run tests
test:
	@echo "Running tests..."
	docker-compose exec app python -m pytest tests/ -v

# Database operations
db-backup:
	@echo "Creating database backup..."
	docker-compose exec db mysqldump -u root -p$(shell grep MYSQL_ROOT_PASSWORD .env | cut -d '=' -f2) investment_portfolio > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup created!"

db-restore:
	@echo "Restoring database from backup..."
	@read -p "Enter backup filename: " backup_file; \
	docker-compose exec -T db mysql -u root -p$(shell grep MYSQL_ROOT_PASSWORD .env | cut -d '=' -f2) investment_portfolio < $$backup_file
	@echo "Database restored!"

# Quick setup
setup:
	@echo "Setting up Investment Portfolio application..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.example .env; \
		echo "Please edit .env file with your configuration!"; \
	fi
	@echo "Building and starting development environment..."
	make build
	make dev
	@echo "Setup complete! Visit http://localhost:8080" 