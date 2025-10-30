# detect.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def featurize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['amount_log'] = np.log1p(df['amount'])
    out_count = df.groupby('sender').size().rename('out_count')
    df = df.merge(out_count.reset_index(), on='sender', how='left')
    return df

def run_isolation(df: pd.DataFrame, contamination=0.02):
    df_feat = featurize(df)
    X = df_feat[['amount_log','out_count']].fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    pred = model.predict(X)
    df_feat['anomaly'] = pred
    df_feat['anomaly_score'] = -model.decision_function(X)
    df_feat['is_suspicious'] = df_feat['anomaly'] == -1
    return df_feat, model
