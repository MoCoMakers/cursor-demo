from flask import Blueprint, render_template, jsonify, request
from app.models import Portfolio, Investment
from app import db
from datetime import datetime

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