"""
Blue Djedi Temple Flask Application
Main application file with proper blueprint organization
"""

from flask import Flask, render_template, request
from flask_cors import CORS
import logging
import os
from blueprints.public import public_bp
from blueprints.admin import admin_bp
from blueprints.api import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='production'):
    """
    Application factory pattern for Flask app creation
    
    Args:
        config_name: Configuration environment (development/production)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.{config_name.capitalize()}Config')
    
    # Initialize CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Root route handler based on domain
    @app.route('/')
    def index():
        """Route based on domain"""
        host = request.headers.get('Host', '')
        
        # Check if this is admin domain
        if host.startswith('admin.'):
            # Redirect to admin blueprint
            return admin_bp.send_static_file('admin')
        else:
            # Show public page
            return render_template('pages/index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server error: {e}")
        return render_template('errors/500.html'), 500
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    # Get environment from ENV variable, default to production
    env = os.getenv('FLASK_ENV', 'production')
    app = create_app(env)
    
    # Get port from environment
    port = int(os.getenv('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=(env == 'development')
    )
