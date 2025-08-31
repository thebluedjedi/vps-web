"""
Configuration settings for Flask application
Separates development and production configurations
"""

import os
from datetime import timedelta

class BaseConfig:
    """Base configuration with common settings"""
    
    # Basic Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
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
    
    # More verbose logging in development
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Less verbose logging in production
    LOG_LEVEL = 'INFO'
    
    # Override secret key from environment
    SECRET_KEY = os.getenv('SECRET_KEY', BaseConfig.SECRET_KEY)

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for tests
    WTF_CSRF_ENABLED = False
