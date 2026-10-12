
const API_BASE = "http://127.0.0.1:8000/api/gold";

let goldChart = null;

const currency = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2
});

function formatPrice(value) {
    return currency.format(value);
}

function formatDate(value) {
    return new Date(value + "T00:00:00").toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}

async function fetchJSON(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
}

function displayChange(element, change, percentage) {
    const sign = change > 0 ? "+" : "";
    const arrow = change > 0 ? "↑" : change < 0 ? "↓" : "—";

    element.textContent =
        `${arrow} ${sign}${formatPrice(change)} (${sign}${percentage.toFixed(2)}%)`;

    element.classList.toggle("negative", change < 0);
}

async function loadLatest() {
    const [latestResult, analysisResult] = await Promise.all([
        fetchJSON(`${API_BASE}/latest`),
        fetchJSON(`${API_BASE}/analysis`)
    ]);

    const latest = latestResult.data;
    const analysis = analysisResult;

    document.getElementById("price24").textContent =
        formatPrice(latest.rate_24k);

    document.getElementById("price22").textContent =
        formatPrice(latest.rate_22k);

    document.getElementById("latestDate").textContent =
        `Updated: ${formatDate(latest.rate_date)}`;

    displayChange(
        document.getElementById("change24"),
        analysis["24k"].change,
        analysis["24k"].percentage_change
    );

    displayChange(
        document.getElementById("change22"),
        analysis["22k"].change,
        analysis["22k"].percentage_change
    );
}

async function loadHistory() {
    const limit = document.getElementById("historyLimit").value;

    const result = await fetchJSON(
        `${API_BASE}/history?limit=${limit}`
    );

    // API returns newest first; charts read left to right.
    const records = [...result.data].reverse();

    renderChart(records);
    renderTable(result.data);

    document.getElementById("chartMessage").textContent =
        `${result.count} historical records loaded.`;
}

function renderChart(records) {
    const ctx = document.getElementById("goldChart");

    const labels = records.map(record => formatDate(record.rate_date));
    const rates24 = records.map(record => record.rate_24k);
    const rates22 = records.map(record => record.rate_22k);

    if (goldChart) {
        goldChart.destroy();
    }

    goldChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "24K Gold (₹/g)",
                    data: rates24,
                    borderColor: "#c18b2d",
                    backgroundColor: "rgba(193, 139, 45, 0.12)",
                    borderWidth: 3,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: "22K Gold (₹/g)",
                    data: rates22,
                    borderColor: "#6576c5",
                    backgroundColor: "rgba(101, 118, 197, 0.06)",
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: "index",
                intersect: false
            },
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    callbacks: {
                        label: context =>
                            `${context.dataset.label}: ${formatPrice(context.parsed.y)}`
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: value =>
                            "₹" + Number(value).toLocaleString("en-IN")
                    },
                    grid: {
                        color: "#edf0f5"
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderTable(records) {
    const table = document.getElementById("historyTable");

    table.replaceChildren();

    if (records.length === 0) {
        const row = table.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 3;
        cell.textContent = "No historical records found.";
        return;
    }

    records.forEach(record => {
        const row = table.insertRow();

        const dateCell = row.insertCell();
        const rate24Cell = row.insertCell();
        const rate22Cell = row.insertCell();

        dateCell.textContent = formatDate(record.rate_date);
        rate24Cell.textContent = formatPrice(record.rate_24k);
        rate22Cell.textContent = formatPrice(record.rate_22k);
    });
}

async function loadDashboard() {
    const status = document.getElementById("connectionStatus");
    const refreshButton = document.getElementById("refreshBtn");
    const chartMessage = document.getElementById("chartMessage");

    refreshButton.disabled = true;
    refreshButton.textContent = "Loading...";

    try {
        await Promise.all([
            loadLatest(),
            loadHistory()
        ]);

        status.textContent = "Connected";
        status.style.color = "#72d5a5";
        chartMessage.textContent = "Historical data loaded successfully.";
    } catch (error) {
        console.error("Dashboard error:", error);

        status.textContent = "Connection failed";
        status.style.color = "#ff9999";

        chartMessage.textContent =
            "Unable to load data. Check that FastAPI is running and the API is accessible.";
    } finally {
        refreshButton.disabled = false;
        refreshButton.textContent = "↻ Refresh Data";
    }
}

document.getElementById("refreshBtn").addEventListener(
    "click",
    loadDashboard
);

document.getElementById("historyLimit").addEventListener(
    "change",
    async () => {
        try {
            await loadHistory();
        } catch (error) {
            console.error(error);
            document.getElementById("chartMessage").textContent =
                "Unable to load historical data.";
        }
    }
);

loadDashboard();
