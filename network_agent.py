# network_agent.py
import networkx as nx
import pandas as pd

def build_graph(df: pd.DataFrame):
    """
    Build a directed transaction graph.
    Each node = account (sender or receiver).
    Each edge = money transfer (weighted by amount).
    """
    G = nx.DiGraph()
    for _, row in df.iterrows():
        sender = row['sender']
        receiver = row['receiver']
        amount = float(row['amount'])
        
        if G.has_edge(sender, receiver):
            G[sender][receiver]['weight'] += amount
            G[sender][receiver]['count'] += 1
        else:
            G.add_edge(sender, receiver, weight=amount, count=1)
    
    return G


def find_suspicious_components(G, min_size=3, weight_threshold=5000):
    """
    Identify groups of connected accounts (subgraphs)
    that may represent laundering or coordinated fraud networks.
    """
    suspects = []
    for comp in nx.weakly_connected_components(G):
        if len(comp) >= min_size:
            subgraph = G.subgraph(comp)
            total_amount = sum(d['weight'] for _, _, d in subgraph.edges(data=True))
            
            if total_amount >= weight_threshold:
                suspects.append({
                    'nodes': list(comp),
                    'total_moved': total_amount,
                    'size': len(comp)
                })
    
    # Sort by total money moved (most suspicious first)
    suspects = sorted(suspects, key=lambda x: x['total_moved'], reverse=True)
    return suspects
