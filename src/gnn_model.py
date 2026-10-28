"""
src/gnn_model.py
Graph Autoencoder (GAE) for Threat Detection.
"""
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.nn import GAE

class GCNEncoder(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, 2 * out_channels)
        self.conv2 = GCNConv(2 * out_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)

def train_gae(data, epochs=200):
    """Trains the Graph Autoencoder to learn normal network behavior."""
    out_channels = 16
    encoder = GCNEncoder(data.num_features, out_channels)
    model = GAE(encoder)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        z = model.encode(data.x, data.edge_index)
        loss = model.recon_loss(z, data.edge_index)
        loss.backward()
        optimizer.step()
        
    return model

def detect_anomalies(model, data):
    """Finds nodes with high reconstruction errors (Anomalies)."""
    model.eval()
    with torch.no_grad():
        z = model.encode(data.x, data.edge_index)
        # Reconstruct the graph
        recon_adj = model.decoder.forward(z, data.edge_index)
        
    # Calculate error per node
    errors = torch.abs(recon_adj - torch.ones_like(recon_adj)).sum(dim=1)
    
    # Normalize errors to 0-1
    errors = (errors - errors.min()) / (errors.max() - errors.min())
    
    return errors.numpy()
