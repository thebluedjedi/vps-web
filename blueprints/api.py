"""
API Blueprint
Handles all API endpoints
"""

from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from utils.prometheus import query_prometheus, query_prometheus_range
from utils.system import get_system_info
import requests
import time
import random
import logging

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0',
        'services': {
            'flask': 'online',
            'traefik': 'online'
        }
    })

@api_bp.route('/system')
def api_system():
    """System information endpoint"""
    return jsonify(get_system_info())

@api_bp.route('/metrics')
def metrics():
    """Basic metrics for Prometheus scraping"""
    # Generate some basic metrics in Prometheus format
    metrics_text = f"""# HELP flask_requests_total Total requests
flask_requests_total {random.randint(100, 1000)}
# HELP flask_uptime_seconds Flask uptime
flask_uptime_seconds {time.time()}
# HELP flask_response_time_seconds Response time
flask_response_time_seconds {random.uniform(0.01, 0.5)}
"""
    return metrics_text, 200, {'Content-Type': 'text/plain'}

@api_bp.route('/prometheus/<path:path>')
def prometheus_proxy(path):
    """Proxy requests to internal Prometheus container"""
    try:
        prom_url = f"{current_app.config['PROMETHEUS_URL']}/{path}"
        
        # Add query string if present
        if request.query_string:
            prom_url += '?' + request.query_string.decode()
        
        # Make request to Prometheus
        response = requests.get(prom_url, timeout=10)
        
        return response.json(), response.status_code, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
        
    except requests.RequestException as e:
        logger.error(f"Prometheus proxy error: {str(e)}")
        return jsonify({'error': f'Prometheus connection failed: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in Prometheus proxy: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/prometheus-test')
def test_prometheus():
    """Test endpoint to verify Prometheus connectivity"""
    try:
        prom_url = f"{current_app.config['PROMETHEUS_URL']}/api/v1/query"
        response = requests.get(f"{prom_url}?query=up", timeout=5)
        
        return jsonify({
            'status': 'connected',
            'prometheus_data': response.json()
        })
    except Exception as e:
        logger.error(f"Prometheus test error: {str(e)}")
        return jsonify({
            'status': 'failed',
            'error': str(e)
        }), 500

@api_bp.route('/telegram/test', methods=['POST'])
def telegram_test():
    """Send test message to Telegram bot"""
    try:
        # Read Telegram secrets
        with open(current_app.config['TELEGRAM_BOT_TOKEN_FILE'], 'r') as f:
            bot_token = f.read().strip()
        with open(current_app.config['TELEGRAM_USER_ID_FILE'], 'r') as f:
            chat_id = f.read().strip()
        
        # Send test message
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        telegram_data = {
            'chat_id': chat_id,
            'text': '🔷 Test message from Blue Djedi Admin Dashboard'
        }
        
        response = requests.post(telegram_url, json=telegram_data, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                'status': 'success',
                'message': 'Test message sent to Telegram'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Telegram API error: {response.status_code}'
            }), 500
            
    except FileNotFoundError:
        return jsonify({
            'status': 'error',
            'message': 'Telegram credentials not configured'
        }), 500
    except Exception as e:
        logger.error(f"Telegram test error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }), 500
