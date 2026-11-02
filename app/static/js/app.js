// HealthPulse Main Client-Side Application Script

document.addEventListener("DOMContentLoaded", () => {
    // Sidebar toggle
    const sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", () => {
            document.getElementById("sidebar-wrapper").classList.toggle("d-none");
        });
    }
});

function showAlert(message, type = "success") {
    const alertBox = document.getElementById("alertBox");
    if (!alertBox) return;

    const alertEl = document.createElement("div");
    alertEl.className = `alert alert-${type} alert-dismissible fade show shadow-sm`;
    alertEl.role = "alert";
    alertEl.innerHTML = `
        <strong>${type === "danger" ? "Error: " : "Notice: "}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertBox.innerHTML = "";
    alertBox.appendChild(alertEl);

    setTimeout(() => {
        alertEl.classList.remove("show");
        alertEl.remove();
    }, 5000);
}

async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...options,
        });
        const json = await response.json();
        if (!response.ok) {
            const err = json.error || json.message || "An error occurred";
            throw new Error(err);
        }
        return json;
    } catch (err) {
        showAlert(err.message, "danger");
        throw err;
    }
}
