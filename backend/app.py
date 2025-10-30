# app.py
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
# In a real hackathon, you’d replace this with an actual ML model or agent system.

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
    # Simple logic (can later connect to your AI Agent)
    risk_score = 0

    # Rules (you can expand later)
    if tx.amount > 10000:
        risk_score += 40
    if tx.sender == tx.receiver:
        risk_score += 30
    if "urgent" in tx.desc.lower() or "transfer quickly" in tx.desc.lower():
        risk_score += 20

    risk_score += random.randint(0, 10)

    # Interpret results
    if risk_score < 30:
        result = "✅ Transaction looks safe."
        explanation = "No unusual patterns detected."
    elif 30 <= risk_score < 60:
        result = "⚠️ Slightly suspicious transaction."
        explanation = "The transaction has moderate risk — monitor for unusual frequency."
    else:
        result = "🚨 High fraud risk detected!"
        explanation = "Large or self-directed transfers may indicate a mule or laundering attempt."

    return {
        "message": result,
        "score": risk_score,
        "explanation": explanation,
    }
