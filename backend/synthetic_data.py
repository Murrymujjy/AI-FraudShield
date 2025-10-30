# synthetic_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_transactions(n=2000, n_accounts=500):
    accounts = [f"ACC{idx}" for idx in range(1, n_accounts+1)]
    start = datetime.utcnow()
    rows = []
    for i in range(n):
        sender = np.random.choice(accounts)
        receiver = np.random.choice(accounts)
        while receiver == sender:
            receiver = np.random.choice(accounts)
        amount = float(np.round(np.random.exponential(scale=2000),2))
        ts = start + timedelta(seconds=int(np.random.exponential(scale=60*60)))
        rows.append({
            "tx_id": f"TX{i}",
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": ts.isoformat()
        })
    df = pd.DataFrame(rows)
    return df

def inject_money_mule(df, leader="ACC1", ring_size=8, txs_per_leader=20):
    ring = [f"ACC{2+i}" for i in range(ring_size)]
    now = pd.to_datetime(df['timestamp']).max() + pd.Timedelta(hours=1)
    rows = []
    for i in range(txs_per_leader):
        for r in ring:
            rows.append({
                "tx_id": f"FRAUD{i}_{r}",
                "sender": leader,
                "receiver": r,
                "amount": float(10000 + np.random.randint(1000)),
                "timestamp": (now + pd.Timedelta(seconds=i*10)).isoformat()
            })
    df2 = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    return df2
