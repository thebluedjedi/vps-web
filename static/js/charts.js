/**
 * Chart.js configurations and utilities
 */

// Chart default configuration
const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#4fc3f7',
            bodyColor: '#e0e0e0',
            borderColor: '#4fc3f7',
            borderWidth: 1
        }
    },
    scales: {
        x: {
            display: false,
            grid: {
                display: false
            }
        },
        y: {
            display: false,
            grid: {
                display: false
            }
        }
    },
    elements: {
        point: {
            radius: 0,
            hoverRadius: 3
        },
        line: {
            tension: 0.4,
            borderWidth: 2
        }
    }
};

// Initialize all charts
function initializeCharts() {
    // CPU Chart
    const cpuCtx = document.getElementById('cpu-chart');
    if (cpuCtx) {
        charts.cpu = new Chart(cpuCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(20),
                datasets: [{
                    data: [],
                    borderColor: '#4fc3f7',
                    backgroundColor: 'rgba(79, 195, 247, 0.1)',
                    fill: true
                }]
            },
            options: chartDefaults
        });
    }
    
    // Memory Chart
    const memoryCtx = document.getElementById('memory-chart');
    if (memoryCtx) {
        charts.memory = new Chart(memoryCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(20),
                datasets: [{
                    data: [],
                    borderColor: '#29b6f6',
                    backgroundColor: 'rgba(41, 182, 246, 0.1)',
                    fill: true
                }]
            },
            options: chartDefaults
        });
    }
    
    // Storage Chart (Doughnut)
    const storageCtx = document.getElementById('storage-chart');
    if (storageCtx) {
        charts.storage = new Chart(storageCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#4fc3f7', 'rgba(255, 255, 255, 0.1)'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
    
    // Network Chart
    const networkCtx = document.getElementById('network-chart');
    if (networkCtx) {
        charts.network = new Chart(networkCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(20),
                datasets: [{
                    data: [],
                    borderColor: '#81c784',
                    backgroundColor: 'rgba(129, 199, 132, 0.1)',
                    fill: true
                }]
            },
            options: chartDefaults
        });
    }
    
    // Response Time Chart
    const responseCtx = document.getElementById('response-chart');
    if (responseCtx) {
        charts.response = new Chart(responseCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(20),
                datasets: [{
                    data: [],
                    borderColor: '#ff9800',
                    backgroundColor: 'rgba(255, 152, 0, 0.1)',
                    fill: true
                }]
            },
            options: chartDefaults
        });
    }
}

// Generate time labels for charts
function generateTimeLabels(count) {
    const labels = [];
    for (let i = count - 1; i >= 0; i--) {
        const time = new Date(Date.now() - i * 30000);
        labels.push(time.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        }));
    }
    return labels;
}

// Update line chart data
function updateLineChart(chart, data) {
    if (!chart || !data) return;
    
    chart.data.datasets[0].data = data;
    chart.update('none'); // Update without animation
}

// Update doughnut chart data
function updateDoughnutChart(chart, used, free) {
    if (!chart) return;
    
    chart.data.datasets[0].data = [used, free];
    chart.update('none');
}
