# agent.py
"""
AI Reasoning Agent for FraudShield
-----------------------------------
This module acts like a smart detective that explains *why* a transaction
might be suspicious. It uses reasoning rules and can be upgraded later
to a full LangChain or LLM-based agent.
"""

import random

class FraudReasoningAgent:
    def __init__(self):
        # You can expand this later with an AI model or API connection.
        self.rules = {
            "large_transfer": "The amount is unusually high for a single transfer, which often indicates laundering or a mule transaction.",
            "same_sender_receiver": "Sender and receiver are the same, suggesting possible internal fund cycling.",
            "urgent_language": "The message contains urgency cues like 'quickly' or 'urgent', often used in scam attempts.",
            "normal": "No known fraud indicators found. Transaction seems normal."
        }

    def analyze(self, sender, receiver, amount, desc):
        explanation = []
        score = 0

        # Rule 1: Large transfer
        if amount > 10000:
            score += 40
            explanation.append(self.rules["large_transfer"])

        # Rule 2: Self-transfer
        if sender == receiver:
            score += 30
            explanation.append(self.rules["same_sender_receiver"])

        # Rule 3: Suspicious words
        if any(x in desc.lower() for x in ["urgent", "quickly", "asap"]):
            score += 20
            explanation.append(self.rules["urgent_language"])

        # Random noise (simulate AI randomness)
        score += random.randint(0, 10)

        if not explanation:
            explanation.append(self.rules["normal"])

        # Risk level
        if score < 30:
            risk = "Low"
        elif 30 <= score < 60:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "risk": risk,
            "score": score,
            "explanation": " ".join(explanation)
        }
