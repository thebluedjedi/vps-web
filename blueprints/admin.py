"""
Admin Blueprint
Handles all admin dashboard routes and functionality
"""

from flask import Blueprint, render_template, jsonify, current_app
from utils.prometheus import query_prometheus, query_prometheus_range
from utils.system import get_system_info
import logging

logger = logging.getLogger(__name__)

# Create blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    """Main admin dashboard view"""
    system_info = get_system_info()
    return render_template('pages/admin.html', system=system_info)

@admin_bp.route('/metrics')
def get_metrics():
    """API endpoint for fetching current metrics"""
    try:
        metrics = {
            'system': get_system_info(),
            'cpu': _get_cpu_metrics(),
            'memory': _get_memory_metrics(),
            'storage': _get_storage_metrics(),
            'network': _get_network_metrics(),
            'services': _get_service_status()
        }
        return jsonify({'status': 'success', 'data': metrics})
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@admin_bp.route('/services/status')
def service_status():
    """Get status of all services"""
    try:
        services = _get_service_status()
        return jsonify({'status': 'success', 'services': services})
    except Exception as e:
        logger.error(f"Error checking services: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def _get_cpu_metrics():
    """Get CPU metrics from Prometheus"""
    try:
        query = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        data = query_prometheus_range(query)
        
        if data and data.get('result'):
            result = data['result'][0] if data['result'] else {}
            values = result.get('values', [])
            
            # Extract just the values for the chart
            chart_data = [float(v[1]) for v in values[-20:]]  # Last 20 points
            current_value = chart_data[-1] if chart_data else 0
            
            return {
                'current': round(current_value, 1),
                'chart_data': chart_data
            }
    except Exception as e:
        logger.error(f"Error getting CPU metrics: {e}")
    
    return {'current': 0, 'chart_data': []}

def _get_memory_metrics():
    """Get memory metrics from Prometheus"""
    try:
        query = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
        data = query_prometheus_range(query)
        
        if data and data.get('result'):
            result = data['result'][0] if data['result'] else {}
            values = result.get('values', [])
            
            chart_data = [float(v[1]) for v in values[-20:]]
            current_value = chart_data[-1] if chart_data else 0
            
            return {
                'current': round(current_value, 1),
                'chart_data': chart_data
            }
    except Exception as e:
        logger.error(f"Error getting memory metrics: {e}")
    
    return {'current': 0, 'chart_data': []}

def _get_storage_metrics():
    """Get storage metrics from Prometheus"""
    try:
        query = '(1 - (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"})) * 100'
        data = query_prometheus(query)
        
        if data and data.get('result'):
            result = data['result'][0] if data['result'] else {}
            value = float(result.get('value', [0, 0])[1])
            
            return {
                'current': round(value, 1),
                'used': value,
                'free': 100 - value
            }
    except Exception as e:
        logger.error(f"Error getting storage metrics: {e}")
    
    return {'current': 0, 'used': 0, 'free': 100}

def _get_network_metrics():
    """Get network traffic metrics"""
    try:
        query = 'rate(node_network_receive_bytes_total{device!="lo"}[5m]) + rate(node_network_transmit_bytes_total{device!="lo"}[5m])'
        data = query_prometheus_range(query)
        
        if data and data.get('result'):
            result = data['result'][0] if data['result'] else {}
            values = result.get('values', [])
            
            # Convert to MB/s
            chart_data = [float(v[1]) / 1024 / 1024 for v in values[-20:]]
            current_value = chart_data[-1] if chart_data else 0
            
            return {
                'current': round(current_value, 2),
                'chart_data': chart_data,
                'unit': 'MB/s'
            }
    except Exception as e:
        logger.error(f"Error getting network metrics: {e}")
    
    return {'current': 0, 'chart_data': [], 'unit': 'MB/s'}

def _get_service_status():
    """Check status of various services"""
    services = {
        'amnezia': False,
        'grafana': False,
        'prometheus': False,
        'portainer': False,
        'telegram': False,
        'librechat': False,
        'n8n': False
    }
    
    try:
        # Check Prometheus directly
        query = 'up'
        data = query_prometheus(query)
        
        if data and data.get('result'):
            for result in data['result']:
                job = result.get('metric', {}).get('job', '')
                value = float(result.get('value', [0, 0])[1])
                
                # Map job names to services
                if 'prometheus' in job:
                    services['prometheus'] = value == 1
                elif 'grafana' in job:
                    services['grafana'] = value == 1
                # Add more mappings as needed
        
        # For now, assume other services are online if Prometheus is working
        if services['prometheus']:
            services['amnezia'] = True
            services['portainer'] = True
            services['telegram'] = True
            services['librechat'] = True
            services['n8n'] = True
            
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
    
    return services
