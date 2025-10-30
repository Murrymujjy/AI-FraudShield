# network_agent.py
import networkx as nx
import pandas as pd

def build_graph(df: pd.DataFrame):
    G = nx.DiGraph()
    for _, r in df.iterrows():
        s = r['sender']; t = r['receiver']; amt = float(r['amount'])
        if G.has_edge(s,t):
            G[s][t]['weight'] += amt
            G[s][t]['count'] += 1
        else:
            G.add_edge(s,t, weight=amt, count=1)
    return G

def find_suspicious_components(G, min_size=3, weight_threshold=5000):
    suspects = []
    for comp in nx.weakly_connected_components(G):
        if len(comp) >= min_size:
            sub = G.subgraph(comp)
            total = sum(d['weight'] for _,_,d in sub.edges(data=True))
            if total >= weight_threshold:
                suspects.append({
                    'nodes': list(comp),
                    'total_moved': total,
                    'size': len(comp)
                })
    suspects = sorted(suspects, key=lambda x: x['total_moved'], reverse=True)
    return suspects
