"""
Prometheus query utilities
Helper functions for interacting with Prometheus
"""

import requests
import logging
from flask import current_app
from datetime import datetime
import math

logger = logging.getLogger(__name__)

def query_prometheus(query):
    """
    Execute an instant query against Prometheus
    
    Args:
        query: PromQL query string
    
    Returns:
        dict: Query result data or None on error
    """
    try:
        url = f"{current_app.config['PROMETHEUS_URL']}/api/v1/query"
        params = {'query': query}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Prometheus query failed with status {response.status_code}")
            return None
        
        data = response.json()
        
        if data.get('status') != 'success':
            logger.error(f"Prometheus query failed: {data.get('error', 'Unknown error')}")
            return None
        
        return data.get('data', {})
        
    except requests.RequestException as e:
        logger.error(f"Prometheus connection error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error querying Prometheus: {e}")
        return None

def query_prometheus_range(query, duration_seconds=600, step=30):
    """
    Execute a range query against Prometheus
    
    Args:
        query: PromQL query string
        duration_seconds: How far back to query (default 10 minutes)
        step: Query resolution in seconds
    
    Returns:
        dict: Query result data or None on error
    """
    try:
        end_time = int(datetime.now().timestamp())
        start_time = end_time - duration_seconds
        
        url = f"{current_app.config['PROMETHEUS_URL']}/api/v1/query_range"
        params = {
            'query': query,
            'start': start_time,
            'end': end_time,
            'step': step
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Prometheus range query failed with status {response.status_code}")
            return None
        
        data = response.json()
        
        if data.get('status') != 'success':
            logger.error(f"Prometheus range query failed: {data.get('error', 'Unknown error')}")
            return None
        
        return data.get('data', {})
        
    except requests.RequestException as e:
        logger.error(f"Prometheus connection error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in range query: {e}")
        return None

def format_bytes(bytes_value):
    """
    Format bytes into human-readable format
    
    Args:
        bytes_value: Number of bytes
    
    Returns:
        str: Formatted string (e.g., "1.5 GB")
    """
    if bytes_value == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = min(int(math.log(bytes_value, 1024)), len(units) - 1)
    
    value = bytes_value / (1024 ** index)
    
    if value >= 10:
        return f"{value:.0f} {units[index]}"
    else:
        return f"{value:.1f} {units[index]}"

def calculate_uptime(boot_time_seconds):
    """
    Calculate uptime from boot time
    
    Args:
        boot_time_seconds: Boot time in seconds since epoch
    
    Returns:
        str: Formatted uptime string
    """
    try:
        current_time = datetime.now().timestamp()
        uptime_seconds = current_time - boot_time_seconds
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except Exception as e:
        logger.error(f"Error calculating uptime: {e}")
        return "Unknown"
