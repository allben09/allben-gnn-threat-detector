"""
src/graph_builder.py
Builds a synthetic corporate network graph using NetworkX.
"""
import networkx as nx
import random
import numpy as np
import torch
from torch_geometric.data import Data
from torch_geometric.utils import from_networkx

np.random.seed(42)
random.seed(42)

def build_corporate_graph(num_users=20, num_servers=5, inject_attack=True):
    """Creates a graph of users and servers. Injects lateral movement if True."""
    G = nx.Graph()

    # 1. Create Nodes
    users = [f"User_{i}" for i in range(num_users)]
    servers = [f"Server_{i}" for i in range(num_servers)]
    
    for u in users:
        G.add_node(u, type="user")
    for s in servers:
        G.add_node(s, type="server")

    # 2. Create Normal Edges (Users log into normal servers)
    for u in users:
        # Each user connects to 1-2 servers they are authorized for
        authorized_servers = random.sample(servers, k=random.randint(1, 2))
        for s in authorized_servers:
            G.add_edge(u, s, weight=random.uniform(1.0, 5.0)) # Normal login frequency

    # 3. Inject Attack (Lateral Movement)
    if inject_attack:
        # A user suddenly connects to a highly sensitive server they shouldn't
        attacker = "User_4"
        sensitive_server = "Server_0"
        G.add_edge(attacker, sensitive_server, weight=50.0) # Massive spike in activity

    return G

def graph_to_pyg(G):
    """Converts a NetworkX graph to a PyTorch Geometric Data object."""
    # Add dummy features for the GNN (e.g., node degree)
    for node in G.nodes():
        G.nodes[node]['x'] = [G.degree(node), 1.0 if G.nodes[node]['type'] == 'user' else 0.0]
        
    data = from_networkx(G)
    data.x = data.x.float()
    return data
