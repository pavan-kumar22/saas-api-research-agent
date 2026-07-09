/* ==========================================================
   Global Variables
========================================================== */

let researchData = [];
let verificationData = [];
let insights = {};


/* ==========================================================
   Utility Functions
========================================================== */

function percentage(value, total) {

    if (total === 0) return 0;

    return ((value / total) * 100).toFixed(1);

}


function groupCount(data, key) {

    const counts = {};

    data.forEach(item => {

        const value = item[key] || "Unknown";

        counts[value] = (counts[value] || 0) + 1;

    });

    return counts;

}


function randomColor(index) {

    const colors = [

        "#3B82F6",
        "#10B981",
        "#F59E0B",
        "#EF4444",
        "#8B5CF6",
        "#06B6D4",
        "#F97316",
        "#84CC16",
        "#EC4899",
        "#6366F1",
        "#14B8A6",
        "#A855F7"

    ];

    return colors[index % colors.length];

}


/* ==========================================================
   CSV Loader
========================================================== */

async function loadCSV(path) {

    const response = await fetch(path);

    const text = await response.text();

    return parseCSV(text);

}


/* ==========================================================
   JSON Loader
========================================================== */

async function loadJSON(path) {

    const response = await fetch(path);

    return await response.json();

}


/* ==========================================================
   CSV Parser
========================================================== */

function parseCSV(csv) {

    const rows = [];

    const lines = csv.trim().split("\n");

    const headers = lines[0]
        .split(",")
        .map(h => h.trim());

    for (let i = 1; i < lines.length; i++) {

        const cols = splitCSV(lines[i]);

        const obj = {};

        headers.forEach((header, index) => {

            obj[header] = cols[index] || "";

        });

        rows.push(obj);

    }

    return rows;

}


/* ==========================================================
   Handles quoted CSV correctly
========================================================== */

function splitCSV(line) {

    const result = [];

    let current = "";

    let insideQuotes = false;

    for (let i = 0; i < line.length; i++) {

        const char = line[i];

        if (char === '"') {

            insideQuotes = !insideQuotes;

            continue;

        }

        if (char === "," && !insideQuotes) {

            result.push(current);

            current = "";

        }

        else {

            current += char;

        }

    }

    result.push(current);

    return result;

}


/* ==========================================================
   Load All Files
========================================================== */

async function loadData() {

    try {

        researchData = await loadCSV("output/research.csv");

    }

    catch {

        console.warn("research.csv not found");

        researchData = [];

    }

    try {

        verificationData = await loadCSV("output/verified.csv");

    }

    catch {

        console.warn("verified.csv not found");

        verificationData = [];

    }

    try {

        insights = await loadJSON("output/insights.json");

    }

    catch {

        console.warn("insights.json not found");

        insights = {};

    }

}
/* ==========================================================
   Badge Generator
========================================================== */

function createBadge(text) {

    const value = (text || "").toLowerCase();

    let cls = "badge-gray";

    if (
        value.includes("oauth") ||
        value.includes("high") ||
        value === "yes"
    ) {
        cls = "badge-blue";
    }

    if (
        value.includes("api key") ||
        value.includes("bearer")
    ) {
        cls = "badge-green";
    }

    if (
        value.includes("unknown")
    ) {
        cls = "badge-yellow";
    }

    if (
        value.includes("failed") ||
        value.includes("error") ||
        value.includes("low") ||
        value === "no"
    ) {
        cls = "badge-red";
    }

    return `<span class="badge ${cls}">${text}</span>`;

}


/* ==========================================================
   Fill Insight Cards
========================================================== */

function populateInsightCards() {

    if (!insights || Object.keys(insights).length === 0) {
        console.warn("Insights not loaded");
        return;
    }

    document.getElementById("totalApps").innerText =
        insights.total_apps ?? 0;

    document.getElementById("oauthPercent").innerText =
        (insights.authentication_percent?.OAuth2 ?? 0) + "%";

    document.getElementById("apikeyPercent").innerText =
        (insights.authentication_percent?.["API Key"] ?? 0) + "%";

    document.getElementById("restPercent").innerText =
        (insights.api_surface_percent?.REST ?? 0) + "%";

    document.getElementById("selfServePercent").innerText =
        (insights.self_serve_percent?.Yes ?? 0) + "%";

    document.getElementById("mcpPercent").innerText =
        (insights.mcp_support_percent?.Yes ?? 0) + "%";

    document.getElementById("highBuildability").innerText =
        (insights.buildability_percent?.High ?? 0) + "%";

    document.getElementById("verifiedPercent").innerText =
        (insights.verification?.verified?.Yes ?? 0) + "%";
}

/* ==========================================================
   Research Table
========================================================== */

function populateResearchTable() {

    const tbody = document.getElementById("researchBody");

    if (!tbody) return;

    tbody.innerHTML = "";

    researchData.forEach((row, index) => {

        const tr = document.createElement("tr");

        const evidence = row.evidence
            ? `<a href="${row.evidence}" target="_blank">Open</a>`
            : "-";

        tr.innerHTML = `

        <td>${index + 1}</td>

        <td><strong>${row.app}</strong></td>

        <td>${row.category}</td>

        <td>${createBadge(row.authentication)}</td>

        <td>${row.api_surface}</td>

        <td>${createBadge(row.self_serve)}</td>

        <td>${createBadge(row.buildability)}</td>

        <td>${row.mcp}</td>

        <td>${row.blocker}</td>

        <td>${evidence}</td>

        <td>${createBadge(row.verified)}</td>

        <td>${createBadge(row.confidence)}</td>

        `;

        tbody.appendChild(tr);

    });

}


/* ==========================================================
   Populate Overview Statistics
========================================================== */

function populateOverviewStats() {

    const stats = document.querySelectorAll(".stat-value");

    if (!stats.length) return;

    const total = researchData.length;

    const verified = researchData.filter(r =>
        (r.verified || "").toLowerCase() === "yes"
    ).length;

    const high = researchData.filter(r =>
        (r.confidence || "").toLowerCase() === "high"
    ).length;

    const rest = researchData.filter(r =>
        (r.api_surface || "").toLowerCase().includes("rest")
    ).length;

    stats[0].innerText = total;

    if (stats[1])
        stats[1].innerText = verified;

    if (stats[2])
        stats[2].innerText = high;

    if (stats[3])
        stats[3].innerText = rest;

}
/* ==========================================================
   Verification Table
========================================================== */

function populateVerificationTable() {

    const tbody = document.getElementById("verificationBody");

    if (!tbody) return;

    tbody.innerHTML = "";

    verificationData.forEach(row => {

        const tr = document.createElement("tr");

        let badge = "badge-gray";

        const result = (row["Result"] || "").toLowerCase();

        if (result.includes("correct"))
            badge = "badge-green";

        else if (result.includes("partial"))
            badge = "badge-yellow";

        else if (result.includes("incorrect"))
            badge = "badge-red";

        tr.innerHTML = `
            <td><strong>${row["App"]}</strong></td>

            <td>${row["Agent Authentication"]}</td>

            <td>${row["Manual Verification"]}</td>

            <td>
                <span class="badge ${badge}">
                    ${row["Result"]}
                </span>
            </td>

            <td>
                <a href="${row["Official Documentation"]}"
                   target="_blank">
                   Open
                </a>
            </td>

            <td>${row["Notes"]}</td>
        `;

        tbody.appendChild(tr);

    });

}


/* ==========================================================
   Live Search
========================================================== */

function searchResearchTable() {

    const input = document
        .getElementById("searchInput");

    if (!input) return;

    input.addEventListener("keyup", function () {

        const filter = this.value.toLowerCase();

        const rows = document.querySelectorAll(
            "#researchBody tr"
        );

        rows.forEach(row => {

            const text = row.innerText.toLowerCase();

            row.style.display =
                text.includes(filter)
                    ? ""
                    : "none";

        });

    });

}


/* ==========================================================
   Download CSV
========================================================== */

function downloadCSV() {

    const button = document.getElementById(
        "downloadCSV"
    );

    if (!button) return;

    button.addEventListener("click", () => {

        window.open(
            "output/research.csv",
            "_blank"
        );

    });

}


/* ==========================================================
   Sort Research Table
========================================================== */

function enableSorting() {

    const headers = document.querySelectorAll(
        "#researchTable thead th"
    );

    headers.forEach((header, index) => {

        header.style.cursor = "pointer";

        header.addEventListener("click", () => {

            sortTable(index);

        });

    });

}


function sortTable(columnIndex) {

    const table = document.getElementById(
        "researchTable"
    );

    const tbody = table.tBodies[0];

    const rows = Array.from(tbody.rows);

    rows.sort((a, b) => {

        const A =
            a.cells[columnIndex]
                .innerText
                .toLowerCase();

        const B =
            b.cells[columnIndex]
                .innerText
                .toLowerCase();

        return A.localeCompare(B);

    });

    tbody.innerHTML = "";

    rows.forEach(row => tbody.appendChild(row));

}


/* ==========================================================
   Scroll Animation
========================================================== */

function revealSections() {

    const observer = new IntersectionObserver(

        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add(
                        "fade-up"
                    );

                }

            });

        },

        {

            threshold: 0.15

        }

    );

    document
        .querySelectorAll("section")
        .forEach(section => {

            observer.observe(section);

        });

}


/* ==========================================================
   Utility
========================================================== */

function initializeTables() {

    populateResearchTable();

    populateVerificationTable();

    searchResearchTable();

    downloadCSV();

    enableSorting();

}
/* ==========================================================
   Chart.js Charts
========================================================== */

let charts = [];


/* ----------------------------------------------------------
   Destroy Existing Charts
---------------------------------------------------------- */

function destroyCharts() {

    charts.forEach(chart => chart.destroy());

    charts = [];

}


/* ----------------------------------------------------------
   Generic Pie Chart
---------------------------------------------------------- */

function createPieChart(canvasId, title, dataObject) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) return;

    const labels = Object.keys(dataObject);

    const values = Object.values(dataObject);

    const colors = labels.map((_, i) => randomColor(i));

    const chart = new Chart(canvas, {

        type: "pie",

        data: {

            labels,

            datasets: [{

                data: values,

                backgroundColor: colors,

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            plugins: {

                title: {

                    display: true,

                    text: title,

                    color: "#fff",

                    font: {
                        size: 18
                    }

                },

                legend: {

                    labels: {

                        color: "#fff"

                    }

                }

            }

        }

    });

    charts.push(chart);

}


/* ----------------------------------------------------------
   Generic Bar Chart
---------------------------------------------------------- */

function createBarChart(canvasId, title, dataObject) {

    const canvas = document.getElementById(canvasId);

    if (!canvas) return;

    const labels = Object.keys(dataObject);

    const values = Object.values(dataObject);

    const colors = labels.map((_, i) => randomColor(i));

    const chart = new Chart(canvas, {

        type: "bar",

        data: {

            labels,

            datasets: [{

                data: values,

                backgroundColor: colors

            }]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {
                        color: "#fff"
                    },

                    grid: {
                        color: "#374151"
                    }

                },

                x: {

                    ticks: {
                        color: "#fff"
                    },

                    grid: {
                        color: "#374151"
                    }

                }

            },

            plugins: {

                legend: {
                    display: false
                },

                title: {

                    display: true,

                    text: title,

                    color: "#fff",

                    font: {
                        size: 18
                    }

                }

            }

        }

    });

    charts.push(chart);

}


/* ----------------------------------------------------------
   Build All Charts
---------------------------------------------------------- */

function initializeCharts() {

    if (!insights || Object.keys(insights).length === 0) {

        console.warn("Insights not loaded");

        return;

    }

    destroyCharts();

    createPieChart(
        "authenticationChart",
        "Authentication Methods",
        insights.authentication_percent
    );

    createPieChart(
        "categoryChart",
        "Application Categories",
        insights.category_percent
    );

    createPieChart(
        "apiSurfaceChart",
        "API Surface",
        insights.api_surface_percent
    );

    createPieChart(
        "selfServeChart",
        "Self Serve",
        insights.self_serve_percent
    );

    createPieChart(
        "mcpChart",
        "MCP Support",
        insights.mcp_support_percent
    );

    createBarChart(
        "buildabilityChart",
        "Buildability",
        insights.buildability_percent
    );

    createBarChart(
        "confidenceChart",
        "Confidence",
        insights.verification.confidence
    );

    createBarChart(
        "blockerChart",
        "Common Blockers",
        insights.common_blockers
    );

}
/* ==========================================================
   Dashboard Initialization
========================================================== */

async function initializeDashboard() {

    console.log("========================================");
    console.log("Loading Dashboard...");
    console.log("========================================");

    await loadData();

    console.log("Research Records :", researchData.length);
    console.log("Verification Records :", verificationData.length);
    console.log("Insights :", insights);

    populateInsightCards();

    populateOverviewStats();

    initializeTables();

    initializeCharts();

    revealSections();

    console.log("========================================");
    console.log("Dashboard Ready");
    console.log("========================================");

}


/* ==========================================================
   Refresh Dashboard
========================================================== */

async function refreshDashboard() {

    await loadData();

    populateInsightCards();

    populateOverviewStats();

    populateResearchTable();

    populateVerificationTable();

    initializeCharts();

}


/* ==========================================================
   Auto Refresh Every 60 Seconds
========================================================== */

setInterval(() => {

    refreshDashboard();

}, 60000);


/* ==========================================================
   Keyboard Shortcuts
========================================================== */

document.addEventListener("keydown", function (event) {

    // Ctrl + F
    if (event.ctrlKey && event.key === "f") {

        event.preventDefault();

        const search = document.getElementById("searchInput");

        if (search) {

            search.focus();

        }

    }

    // Ctrl + R
    if (event.ctrlKey && event.key === "r") {

        event.preventDefault();

        refreshDashboard();

    }

});


/* ==========================================================
   Smooth Navigation
========================================================== */

document.querySelectorAll("nav a").forEach(link => {

    link.addEventListener("click", function (event) {

        event.preventDefault();

        const id = this.getAttribute("href");

        const section = document.querySelector(id);

        if (section) {

            section.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


/* ==========================================================
   Scroll To Top Button (Optional)
========================================================== */

const scrollButton = document.createElement("button");

scrollButton.innerHTML = "↑";

scrollButton.id = "scrollTopBtn";

scrollButton.style.position = "fixed";
scrollButton.style.bottom = "30px";
scrollButton.style.right = "30px";
scrollButton.style.width = "50px";
scrollButton.style.height = "50px";
scrollButton.style.borderRadius = "50%";
scrollButton.style.border = "none";
scrollButton.style.cursor = "pointer";
scrollButton.style.fontSize = "20px";
scrollButton.style.display = "none";
scrollButton.style.background = "#2563eb";
scrollButton.style.color = "white";
scrollButton.style.boxShadow = "0 6px 18px rgba(0,0,0,.35)";
scrollButton.style.zIndex = "999";

document.body.appendChild(scrollButton);

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        scrollButton.style.display = "block";

    }

    else {

        scrollButton.style.display = "none";

    }

});

scrollButton.addEventListener("click", () => {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

});


/* ==========================================================
   Dashboard Start
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    initializeDashboard();

});