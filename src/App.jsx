import React, { useState } from 'react'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleUpload() {
    if (!file) {
      alert("Please choose a CSV file first.")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const res = await fetch(`${BACKEND}/analyze`, {
        method: 'POST',
        body: formData
      })

      const data = await res.json()
      if (data.status === 'success') {
        setResult(data.result)
      } else {
        setError(data.message || 'Analysis failed.')
      }
    } catch (e) {
      console.error(e)
      setError('Failed to connect to backend.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      padding: '2rem',
      fontFamily: 'Inter, sans-serif',
      maxWidth: '800px',
      margin: 'auto',
      textAlign: 'center'
    }}>
      <h1>💡 AI FraudShield</h1>
      <p>Upload a CSV of transactions to detect potential fraud patterns in real-time.</p>

      <input
        type="file"
        accept=".csv"
        onChange={e => setFile(e.target.files[0])}
        style={{ margin: '20px 0' }}
      />

      <br/>
      <button
        onClick={handleUpload}
        disabled={loading}
        style={{
          background: '#007bff',
          color: 'white',
          border: 'none',
          padding: '10px 20px',
          borderRadius: '6px',
          cursor: 'pointer'
        }}
      >
        {loading ? 'Analyzing...' : 'Analyze CSV'}
      </button>

      {error && (
        <div style={{ color: 'red', marginTop: '1rem' }}>
          ❌ {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '2rem', textAlign: 'left' }}>
          <h2>📊 Analysis Summary</h2>
          <p><strong>Total Transactions:</strong> {result.summary.total_transactions}</p>
          <p><strong>Flagged:</strong> {result.summary.flagged_count} ({result.summary.flagged_percent}%)</p>

          <h3>🧩 AI Explanation</h3>
          <p style={{
            background: '#f7f7f7',
            padding: '1rem',
            borderRadius: '8px',
            whiteSpace: 'pre-wrap'
          }}>
            {result.explanation}
          </p>

          <h3>⚠️ Flagged Transactions (Top 10)</h3>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '1rem',
            fontSize: '0.9rem'
          }}>
            <thead>
              <tr style={{ background: '#e9ecef' }}>
                <th>Tx ID</th>
                <th>Sender</th>
                <th>Receiver</th>
                <th>Amount</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {result.flagged_data.slice(0,10).map((tx, i) => (
                <tr key={i} style={{ borderBottom: '1px solid #ddd' }}>
                  <td>{tx.tx_id}</td>
                  <td>{tx.sender}</td>
                  <td>{tx.receiver}</td>
                  <td>{tx.amount}</td>
                  <td>{tx.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
