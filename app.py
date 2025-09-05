"""
Blue Djedi Public Website
Flask application for public website only
"""

from flask import Flask, render_template
from flask_cors import CORS
import logging
from blueprints.public import public_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object('config.ProductionConfig')
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprint
    app.register_blueprint(public_bp)
    
    # Root route shows public page
    @app.route('/')
    def index():
        return render_template('pages/index.html')
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
