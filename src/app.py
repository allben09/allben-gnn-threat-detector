"""
src/app.py
Streamlit UI for GNN Threat Detection with interactive Network Graph.
"""
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

from graph_builder import build_corporate_graph, graph_to_pyg
from gnn_model import train_gae, detect_anomalies

st.set_page_config(page_title="GNN Threat Detector", layout="wide")

st.title("🕸️ Allben GNN Threat Detector")
st.caption("Graph Neural Network for Lateral Movement & APT Detection")

# Sidebar
st.sidebar.header("⚙️ Graph Configuration")
num_users = st.sidebar.slider("Number of Users", 10, 50, 20)
inject_attack = st.sidebar.checkbox("Inject Lateral Movement Attack", value=True)

# Main Execution
G = build_corporate_graph(num_users=num_users, inject_attack=inject_attack)
data = graph_to_pyg(G)

if st.button("▶️ Train GNN & Detect Threats"):
    with st.spinner("Training Graph Autoencoder..."):
        model = train_gae(data, epochs=100)
        
    with st.spinner("Analyzing Graph Topology..."):
        anomalies = detect_anomalies(model, data)
        
    # Map anomalies to node names
    node_names = list(G.nodes())
    anomaly_dict = {node_names[i]: anomalies[i] for i in range(len(node_names))}
    
    # Threshold for flagging
    THRESHOLD = 0.7
    flagged_nodes = {k: v for k, v in anomaly_dict.items() if v > THRESHOLD}
    
    st.success("✅ GNN Analysis Complete!")
    
    # Display Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Nodes Analyzed", len(node_names))
    col2.metric("🚨 Anomalies Detected", len(flagged_nodes), delta_color="inverse")
    
    # Render Interactive Graph with PyVis
    st.subheader("🕸️ Network Graph Visualization")
    st.markdown("*Red nodes indicate high reconstruction error (Potential Threats).*")
    
    net = Network(height="600px", width="100%", bgcolor="#0F172A", font_color="white")
    
    for node in G.nodes():
        score = anomaly_dict.get(node, 0)
        if score > THRESHOLD:
            color = "#EF4444" # Red for anomaly
            title = f"ANOMALY SCORE: {score:.2f}"
            size = 30
        else:
            color = "#38BDF8" if G.nodes[node]['type'] == 'user' else "#10B981"
            title = "Normal"
            size = 20
            
        net.add_node(node, label=node, color=color, title=title, size=size)
        
    for edge in G.edges(data=True):
        net.add_edge(edge[0], edge[1])

    # Generate HTML and display in Streamlit
    net.save_graph("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=650)
    
    # Table of Anomalies
    if flagged_nodes:
        st.subheader("🚨 Flagged Anomalies")
        df = pd.DataFrame(list(flagged_nodes.items()), columns=["Node", "Anomaly Score"])
        df = df.sort_values(by="Anomaly Score", ascending=False)
        st.dataframe(df, use_container_width=True)
