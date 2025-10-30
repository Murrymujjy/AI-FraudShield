# orchestrator.py
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from .detect import run_isolation
from .network_agent import build_graph, find_suspicious_components
from .explain_agent import explain_case

router = APIRouter()

class TxIn(BaseModel):
    tx_id: str
    sender: str
    receiver: str
    amount: float
    timestamp: str

BUFFER = []

@router.post('/ingest')
async def ingest(tx: TxIn):
    BUFFER.append(tx.dict())
    df = pd.DataFrame(BUFFER)
    df_feat, model = run_isolation(df, contamination=0.02)
    flagged = df_feat[df_feat['is_suspicious']]
    if not flagged.empty:
        G = build_graph(df)
        clusters = find_suspicious_components(G)
        explanation = explain_case(flagged, clusters)
        return {
            'alert': True,
            'flagged_count': int(flagged.shape[0]),
            'flagged_sample': flagged[['tx_id','sender','receiver','amount','anomaly_score']].head(10).to_dict(orient='records'),
            'clusters': clusters,
            'explanation': explanation
        }
    return {'alert': False, 'flagged_count': 0}
