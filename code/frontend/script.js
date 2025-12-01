const API_URL = "http://127.0.0.1:8000/classify";

function renderProbs(probabilities) {
    const probsEl = document.getElementById("probs");
    probsEl.innerHTML = "";
    if (!probabilities) {
        probsEl.textContent = "Classifier did not return probabilities.";
        return;
    }
    const entries = Object.entries(probabilities);
    entries.sort((a, b) => b[1] - a[1]);
    entries.forEach(([label, val]) => {
        const row = document.createElement("div");
        row.className = "prob-row";

        const name = document.createElement("div");
        name.className = "prob-label";
        name.textContent = label;

        const bar = document.createElement("div");
        bar.className = "prob-bar";
        const fill = document.createElement("div");
        fill.className = "prob-fill";
        fill.style.width = `${(val * 100).toFixed(0)}%`;
        bar.appendChild(fill);

        const pct = document.createElement("div");
        pct.className = "prob-val";
        pct.textContent = `${(val * 100).toFixed(1)}%`;

        row.appendChild(name);
        row.appendChild(bar);
        row.appendChild(pct);
        probsEl.appendChild(row);
    });
}

async function classify() {
    const textarea = document.getElementById("message");
    const status = document.getElementById("status");
    const results = document.getElementById("results");
    const predictedEl = document.getElementById("predicted");

    const raw = textarea.value || "";
    const normalized = raw.replace(/\r\n/g, "\n");

    if (!normalized.trim()) {
        status.textContent = "Please enter an email.";
        return;
    }

    status.textContent = "Classifying...";
    results.classList.add("hidden");

    try {
        const resp = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: normalized })
        });
        if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            throw new Error(err.detail || `HTTP ${resp.status}`);
        }
        const data = await resp.json();
        predictedEl.textContent = `Predicted class: ${data.predicted_class}`;
        renderProbs(data.probabilities);
        results.classList.remove("hidden");
        status.textContent = "Done.";
    } catch (e) {
        status.textContent = `Error: ${e.message}`;
    }
}

function clearInput() {
    const textarea = document.getElementById("message");
    const status = document.getElementById("status");
    const results = document.getElementById("results");
    const probs = document.getElementById("probs");
    const predicted = document.getElementById("predicted");
    textarea.value = "";
    status.textContent = "";
    predicted.textContent = "";
    probs.innerHTML = "";
    results.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("classifyBtn").addEventListener("click", classify);
    document.getElementById("clearBtn").addEventListener("click", clearInput);
});