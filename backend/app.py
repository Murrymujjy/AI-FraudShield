

# app.py
from agent import FraudReasoningAgent
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="AI FraudShield API")

# Allow frontend (Netlify/Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- MODEL SIMULATION -----

class Transaction(BaseModel):
    sender: int
    receiver: int
    amount: float
    desc: str = ""

@app.get("/")
def home():
    return {"message": "Welcome to AI FraudShield API!"}

@app.post("/api/check")
def check_transaction(tx: Transaction):
    agent = FraudReasoningAgent()
    result = agent.analyze(tx.sender, tx.receiver, tx.amount, tx.desc)

    # Interpret results
    if result["risk"] == "Low":
        msg = "✅ Transaction looks safe."
    elif result["risk"] == "Medium":
        msg = "⚠️ Slightly suspicious transaction."
    else:
        msg = "🚨 High fraud risk detected!"

    return {
        "message": msg,
        "score": result["score"],
        "explanation": result["explanation"]
    }

# app.py
from agent import FraudReasoningAgent
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="AI FraudShield API")

# Allow frontend (Netlify/Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- MODEL SIMULATION -----

class Transaction(BaseModel):
    sender: int
    receiver: int
    amount: float
    desc: str = ""

@app.get("/")
def home():
    return {"message": "Welcome to AI FraudShield API!"}

from network_agent import build_graph, find_suspicious_components
import pandas as pd

@app.post("/analyze-network")
def analyze_network(payload: dict):
    try:
        data = payload.get("transactions")
        if not data:
            raise HTTPException(status_code=400, detail="Missing transaction data list")
        
        df = pd.DataFrame(data)
        G = build_graph(df)
        suspects = find_suspicious_components(G)
        return {"suspect_networks": suspects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from detect import run_isolation
import pandas as pd

@app.post("/detect-anomalies")
def detect_anomalies(payload: dict):
    try:
        data = payload.get("transactions")
        if not data:
            raise HTTPException(status_code=400, detail="Missing transaction data list")
        
        df = pd.DataFrame(data)
        results, _ = run_isolation(df)
        suspicious = results[results['is_suspicious'] == True]
        return {
            "total_transactions": len(df),
            "suspicious_count": len(suspicious),
            "suspicious_samples": suspicious.head(10).to_dict(orient="records"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



