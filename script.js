// script.js
const BASE_URL = "https://your-backend.onrender.com"; // replace after deployment

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
