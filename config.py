#cd /opt/vps/web

# Backup the broken one
#cp config.py config.py.broken

# Create clean config.py
#cat > config.py << 'EOF'
"""
Configuration settings for Flask application
Separates development and production configurations
"""
import os
from datetime import timedelta

# Secrets helper function
def read_secret_file(filepath, fallback=None):
    """Read secret from file with fallback"""
    try:
        with open(filepath, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return fallback

class BaseConfig:
    """Base configuration with common settings"""
    # Basic Flask config
    SECRET_KEY = read_secret_file('/run/secrets/flask_secret_key', 'dev-fallback-only')
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Template auto-reload
    TEMPLATES_AUTO_RELOAD = True
    
    # JSON settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Telegram settings (from Docker secrets)
    TELEGRAM_BOT_TOKEN_FILE = '/run/secrets/telegram_bot_token'
    TELEGRAM_USER_ID_FILE = '/run/secrets/telegram_user_id'
    
    # Prometheus settings
    PROMETHEUS_URL = 'http://vps-prometheus:9090'
    
    # Service URLs (for internal Docker network)
    GRAFANA_URL = 'http://vps-grafana:3000'
    PORTAINER_URL = 'http://portainer:9000'
    TRAEFIK_URL = 'http://traefik:8080'

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
#EOF