import streamlit as st
import pandas as pd
import sys
sys.path.append('..')  # to import backend.app if running from streamlit_demo folder
from backend.app.synthetic_data import generate_transactions, inject_money_mule
from backend.app.detect import run_isolation
from backend.app.network_agent import build_graph
from pyvis.network import Network

st.title('AI FraudShield — Local Demo')

if st.button('Generate demo'):
    df = generate_transactions(800,300)
    df = inject_money_mule(df, leader='ACC1', ring_size=6, txs_per_leader=8)
    st.dataframe(df.head(50))
    df_feat, model = run_isolation(df)
    flagged = df_feat[df_feat['is_suspicious']]
    st.write('Flagged transactions')
    st.dataframe(flagged.head(50))

    G = build_graph(df)
    net = Network(height='500px', width='100%')
    net.from_nx(G)
    net.show('graph.html')
    HtmlFile = open('graph.html','r',encoding='utf-8')
    components = HtmlFile.read()
    st.components.v1.html(components, height=600, scrolling=True)
