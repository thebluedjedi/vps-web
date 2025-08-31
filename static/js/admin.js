/**
 * Admin Dashboard JavaScript
 * Handles metrics updates and dashboard functionality
 */

// Chart instances
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin dashboard initialized');
    
    // Initialize charts
    initializeCharts();
    
    // Load initial data
    refreshMetrics();
    
    // Set up auto-refresh every 30 seconds
    setInterval(refreshMetrics, 30000);
    
    // Check tunnel status
    checkTunnelStatus();
    setInterval(checkTunnelStatus, 10000);
});

// Refresh all metrics
async function refreshMetrics() {
    const btn = document.getElementById('refreshBtn');
    const icon = document.getElementById('refreshIcon');
    
    // Show loading state
    if (btn) btn.disabled = true;
    if (icon) icon.classList.add('animate-spin');
    
    try {
        // Fetch metrics from API
        const response = await fetch('/admin/metrics');
        const data = await response.json();
        
        if (data.status === 'success') {
            updateDashboard(data.data);
        }
    } catch (error) {
        console.error('Failed to refresh metrics:', error);
    } finally {
        // Reset loading state
        if (btn) btn.disabled = false;
        if (icon) icon.classList.remove('animate-spin');
    }
}

// Update dashboard with new data
function updateDashboard(data) {
    // Update system info
    if (data.system) {
        // Uptime
        if (data.system.uptime) {
            updateElement('uptime-value', data.system.uptime);
            updateElement('uptime-display', data.system.uptime_short || data.system.uptime);
        }
        
        // CPU
        if (data.system.cpu) {
            updateElement('cpu-value', `${data.system.cpu.percent}%`);
        }
        
        // Memory
        if (data.system.memory) {
            updateElement('memory-value', `${data.system.memory.percent.toFixed(1)}%`);
        }
        
        // Storage
        if (data.system.disk) {
            updateElement('storage-value', `${data.system.disk.percent.toFixed(1)}%`);
        }
    }
    
    // Update charts
    if (data.cpu && charts.cpu) {
        updateLineChart(charts.cpu, data.cpu.chart_data);
    }
    
    if (data.memory && charts.memory) {
        updateLineChart(charts.memory, data.memory.chart_data);
    }
    
    if (data.storage && charts.storage) {
        updateDoughnutChart(charts.storage, data.storage.used, data.storage.free);
    }
    
    if (data.network && charts.network) {
        updateLineChart(charts.network, data.network.chart_data);
        updateElement('network-value', `${data.network.current} ${data.network.unit}`);
    }
    
    // Update service status
    if (data.services) {
        updateServiceStatus(data.services);
    }
}

// Update element text
function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

// Update service status indicators
function updateServiceStatus(services) {
    Object.keys(services).forEach(service => {
        const light = document.getElementById(`${service}-light`);
        if (light) {
            light.classList.remove('online', 'offline', 'pending');
            light.classList.add(services[service] ? 'online' : 'offline');
        }
    });
}

// Check SSH tunnel status
function checkTunnelStatus() {
    const services = [
        { name: 'traefik', port: 8080 },
        { name: 'grafana', port: 3000 },
        { name: 'portainer', port: 9000 }
    ];
    
    services.forEach(service => {
        fetch(`http://localhost:${service.port}/`, { mode: 'no-cors' })
            .then(() => {
                const status = document.getElementById(`${service.name}-status`);
                if (status) status.classList.add('online');
            })
            .catch(() => {
                const status = document.getElementById(`${service.name}-status`);
                if (status) status.classList.remove('online');
            });
    });
}

// In static/js/admin.js
// Enhance the openTunnel function

function openTunnel(service, localPort, remotePort, path = '') {
    const tunnelCmd = `ssh -L ${localPort}:localhost:${remotePort} -p 2222 root@161.97.82.115`;
    const fullUrl = `http://localhost:${localPort}${path}`;
    
    // Attempt to open the URL
    const newWindow = window.open(fullUrl, '_blank');
    
    // If opening fails or URL is not accessible, show tunnel instructions
    setTimeout(() => {
        fetch(fullUrl, { mode: 'no-cors', cache: 'no-cache' })
            .catch(() => {
                if (newWindow) {
                    newWindow.close();
                }
                
                Swal.fire({
                    title: `SSH Tunnel Required for ${service}`,
                    html: `
                        <p>Run the following SSH tunnel command:</p>
                        <pre><code>${tunnelCmd}</code></pre>
                        <p>Then visit: <a href="${fullUrl}" target="_blank">${fullUrl}</a></p>
                    `,
                    icon: 'info',
                    confirmButtonText: 'Copy SSH Command',
                    showCancelButton: true,
                    cancelButtonText: 'Close'
                }).then((result) => {
                    if (result.isConfirmed) {
                        navigator.clipboard.writeText(tunnelCmd).then(() => {
                            Swal.fire('Copied!', 'SSH command copied to clipboard.', 'success');
                        });
                    }
                });
            });
    }, 100);
}

// Update the dashboard links to use new tunnel function
document.addEventListener('DOMContentLoaded', () => {
    // Tunnel links with specific configurations
    document.getElementById('grafana-tunnel-link').addEventListener('click', (e) => {
        e.preventDefault();
        openTunnel('Grafana', 3000, 3000, '/');
    });

    document.getElementById('traefik-tunnel-link').addEventListener('click', (e) => {
        e.preventDefault();
        openTunnel('Traefik', 8080, 8080, '/dashboard');
    });

    document.getElementById('portainer-tunnel-link').addEventListener('click', (e) => {
        e.preventDefault();
        openTunnel('Portainer', 9000, 9000, '/');
    });
});