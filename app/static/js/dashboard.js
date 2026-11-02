// HealthPulse Analytics Dashboard Visualizations

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const statsRes = await apiRequest("/api/dashboard/stats");
        const billingRes = await apiRequest("/api/reports/monthly-billing");
        const apptStatusRes = await apiRequest("/api/reports/appointment-status");

        if (billingRes && billingRes.data) {
            renderBillingChart(billingRes.data);
        }

        if (apptStatusRes && apptStatusRes.data && apptStatusRes.data.status_distribution) {
            renderStatusChart(apptStatusRes.data.status_distribution);
        }
    } catch (e) {
        console.error("Dashboard metrics failed to load", e);
    }
});

function renderBillingChart(data) {
    const ctx = document.getElementById("billingChart");
    if (!ctx) return;

    const labels = data.map(d => d.billing_month);
    const billed = data.map(d => d.total_billed);
    const collected = data.map(d => d.total_collected);
    const outstanding = data.map(d => d.total_outstanding);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Billed ($)",
                    data: billed,
                    backgroundColor: "#0d6efd",
                    borderRadius: 4,
                },
                {
                    label: "Collected ($)",
                    data: collected,
                    backgroundColor: "#198754",
                    borderRadius: 4,
                },
                {
                    label: "Outstanding ($)",
                    data: outstanding,
                    backgroundColor: "#dc3545",
                    borderRadius: 4,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: v => "$" + v }
                }
            }
        }
    });
}

function renderStatusChart(data) {
    const ctx = document.getElementById("statusChart");
    if (!ctx) return;

    const labels = data.map(d => d.status);
    const counts = data.map(d => d.count);

    const colors = {
        "COMPLETED": "#198754",
        "SCHEDULED": "#0dcaf0",
        "CONFIRMED": "#0d6efd",
        "CANCELLED": "#dc3545",
        "NO_SHOW": "#ffc107"
    };

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: labels.map(l => colors[l] || "#6c757d"),
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "right" }
            }
        }
    });
}
