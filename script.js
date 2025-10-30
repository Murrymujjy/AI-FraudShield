// script.js
const BASE_URL = "https://your-backend.onrender.com"; // replace with your Render backend URL

// --- Single Transaction Detection ---
document.getElementById("detectBtn").addEventListener("click", async () => {
  const transaction = document.getElementById("transaction").value.trim();
  if (!transaction) return alert("Please enter transaction details.");

  const response = await fetch(`${BASE_URL}/detect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transaction }),
  });

  const data = await response.json();
  document.getElementById("result").innerHTML = `
    <strong>Result:</strong> ${data.result.label}<br>
    <strong>Risk Score:</strong> ${data.result.risk_score}
  `;
});

// --- Explain Transaction ---
document.getElementById("explainBtn").addEventListener("click", async () => {
  const transaction = document.getElementById("transaction").value.trim();
  if (!transaction) return alert("Please enter transaction details.");

  const response = await fetch(`${BASE_URL}/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transaction }),
  });

  const data = await response.json();
  document.getElementById("result").innerHTML = `
    <strong>Explanation:</strong> ${data.explanation}
  `;
});

// --- Network Fraud Detection ---
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const rawInput = document.getElementById("networkData").value.trim();
  if (!rawInput) return alert("Please paste transaction data in JSON format.");

  let transactions;
  try {
    transactions = JSON.parse(rawInput);
  } catch {
    return alert("Invalid JSON format. Please fix and try again.");
  }

  const response = await fetch(`${BASE_URL}/analyze-network`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transactions }),
  });

  const data = await response.json();
  const suspects = data.suspect_networks;

  if (!suspects || suspects.length === 0) {
    document.getElementById("networkResult").innerHTML = "No suspicious networks found.";
    document.getElementById("networkGraph").innerHTML = "";
    return;
  }

  // Display text summary
  document.getElementById("networkResult").innerHTML = `
    <strong>Suspicious Networks Found:</strong> ${suspects.length}<br>
    <pre>${JSON.stringify(suspects, null, 2)}</pre>
  `;

  // --- Plotly Visualization ---
  const edges = [];
  const nodes = new Set();

  transactions.forEach(t => {
    edges.push({ x: [t.sender, t.receiver], y: [0, 1] });
    nodes.add(t.sender);
    nodes.add(t.receiver);
  });

  const nodeTrace = {
    x: Array.from(nodes),
    y: Array(nodes.size).fill(0),
    text: Array.from(nodes),
    mode: "markers+text",
    type: "scatter",
    textposition: "top center",
    marker: { size: 12, color: "#007bff" },
  };

  const edgeTraces = transactions.map(t => ({
    x: [t.sender, t.receiver],
    y: [0, 1],
    mode: "lines",
    line: { width: 2, color: "#ccc" },
  }));

  const layout = {
    title: "Transaction Network",
    showlegend: false,
    xaxis: { showgrid: false, zeroline: false, showticklabels: false },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false },
  };

  Plotly.newPlot("networkGraph", [...edgeTraces, nodeTrace], layout);
});
