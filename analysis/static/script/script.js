// Leave Chart
new Chart(document.getElementById('leaveChart'), {
    type: 'doughnut',
    data: {
        labels: leave_data.map(d => d.type),
        datasets: [{
            data: leave_data.map(d => d.count),
            backgroundColor: ['#FF9F40', '#FF6384', '#36A2EB', '#FFCD56']
        }]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
});

// Job Role Chart
new Chart(document.getElementById('jobRoleChart'), {
    type: 'bar',
    data: {
        labels: job_roles.map(d => d.role),
        datasets: [{
            label: 'Employees',
            data: job_roles.map(d => d.count),
            backgroundColor: '#4BC0C0'
        }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
});

// Tenure Chart
new Chart(document.getElementById('tenureChart'), {
    type: 'bar',
    data: {
        labels: tenure_data.map(d => d.range),
        datasets: [{
            label: 'Employees',
            data: tenure_data.map(d => d.count),
            backgroundColor: '#9966FF'
        }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
});

// Location Chart
new Chart(document.getElementById('locationChart'), {
    type: 'pie',
    data: {
        labels: work_location_data.map(d => d.type),
        datasets: [{
            data: work_location_data.map(d => d.count),
            backgroundColor: ['#36A2EB', '#FF6384', '#4BC0C0']
        }]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
});


