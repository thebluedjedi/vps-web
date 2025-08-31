"""
System monitoring utilities
Functions for getting system information
"""

import psutil
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_system_info():
    """
    Get comprehensive system information
    
    Returns:
        dict: System metrics including CPU, memory, disk, and uptime
    """
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent,
            'total_gb': round(memory.total / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2)
        }
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_info = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2)
        }
        
        # Network I/O
        net_io = psutil.net_io_counters()
        network_info = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
        
        # System uptime
        boot_time = psutil.boot_time()
        uptime_seconds = datetime.now().timestamp() - boot_time
        uptime_delta = timedelta(seconds=uptime_seconds)
        
        # Format uptime as readable string
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            uptime_str = f"{days}d {hours}h {minutes}m"
            uptime_short = f"{days}d {hours}h"
        elif hours > 0:
            uptime_str = f"{hours}h {minutes}m"
            uptime_short = uptime_str
        else:
            uptime_str = f"{minutes}m"
            uptime_short = uptime_str
        
        # Process count
        process_count = len(psutil.pids())
        
        return {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': memory_info,
            'disk': disk_info,
            'network': network_info,
            'uptime': uptime_str,
            'uptime_short': uptime_short,
            'uptime_seconds': int(uptime_seconds),
            'process_count': process_count,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_docker_stats():
    """
    Get Docker container statistics
    
    Returns:
        dict: Container information and stats
    """
    try:
        import docker
        client = docker.from_env()
        
        containers = []
        for container in client.containers.list():
            stats = container.stats(stream=False)
            containers.append({
                'name': container.name,
                'status': container.status,
                'id': container.short_id,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'stats': {
                    'cpu_percent': _calculate_cpu_percent(stats),
                    'memory_usage': stats['memory_stats'].get('usage', 0),
                    'memory_limit': stats['memory_stats'].get('limit', 0)
                }
            })
        
        return {'containers': containers}
        
    except ImportError:
        logger.warning("Docker SDK not installed")
        return {'error': 'Docker SDK not available'}
    except Exception as e:
        logger.error(f"Error getting Docker stats: {e}")
        return {'error': str(e)}

def _calculate_cpu_percent(stats):
    """
    Calculate CPU percentage from Docker stats
    
    Args:
        stats: Docker container stats
    
    Returns:
        float: CPU usage percentage
    """
    try:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                   stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                      stats['precpu_stats']['system_cpu_usage']
        
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * 100.0
            return round(cpu_percent, 2)
    except (KeyError, TypeError, ZeroDivisionError):
        pass
    
    return 0.0
