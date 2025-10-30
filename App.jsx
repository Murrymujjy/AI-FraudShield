import React, { useState } from 'react'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App(){
  const [txs, setTxs] = useState([])
  const [result, setResult] = useState(null)

  async function generateAndIngest(){
    const res = await fetch(`${BACKEND}/generate`)
    const data = await res.json()
    setTxs(data)
    for(let i=0;i<Math.min(40,data.length);i++){
      await fetch(`${BACKEND}/ingest`, {
        method: 'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data[i])
      }).then(r=>r.json()).then(j=>{
        if(j.alert){ setResult(j) }
      }).catch(e=>console.error(e))
    }
  }

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>AI FraudShield — Frontend Demo</h1>
      <button onClick={generateAndIngest}>Generate & Run Demo</button>
      {result ? (
        <div style={{marginTop:20}}>
          <h2>Alert!</h2>
          <p>Flagged count: {result.flagged_count}</p>
          <pre style={{whiteSpace:'pre-wrap'}}>{result.explanation}</pre>
        </div>
      ) : <p>No alerts yet — run the demo.</p>}
    </div>
  )
}
