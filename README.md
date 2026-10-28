<div align="center">

# 🕸️ allben-gnn-threat-detector

### *Graph Neural Networks for Advanced Persistent Threat (APT) Detection*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![PyG](https://img.shields.io/badge/PyTorch_Geometric-2.3+-3C2179?style=for-the-badge)](https://pyg.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph_Builder-2E8B57?style=for-the-badge)](https://networkx.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**A state-of-the-art Threat Detection system built by [Allben Rakgoale](https://github.com/allben09). Unlike traditional Intrusion Detection Systems (IDS) that analyze packets in isolation, this project models the entire corporate network as a Graph and uses a Graph Autoencoder (GAE) to detect lateral movement and APTs.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The APT / Lateral Movement Problem](#-the-apt--lateral-movement-problem)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [ML Model Details](#-ml-model-details)
- [Quick Start](#-quick-start)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Author](#-author)

---

## 🔍 Overview

Traditional Machine Learning models for cybersecurity (like Random Forests or SVMs) treat network traffic as **tabular data** (rows and columns of features). While effective for known attacks, they fail to understand the **topology** of a network.

Advanced Persistent Threats (APTs) and insider threats rely on **lateral movement** — pivoting from one server to another until they reach high-value data. 

**allben-gnn-threat-detector** solves this by treating the network as a **Graph**:
- **Nodes**: Users, Servers, IPs
- **Edges**: Logins, Connections, File Access

By training a **Graph Autoencoder (GAE)** on the normal topology, the system detects anomalies when an attacker creates unusual connections (e.g., an HR user suddenly connecting to a Domain Controller at 2 AM).

---

## 🎯 The APT / Lateral Movement Problem

| Challenge | How Traditional IDS Fail | How GNNs Solve It |
| :--- | :--- | :--- |
| **Lateral Movement** | Packet inspection can't see the "big picture" of a user moving across servers. | Graph edges reveal the exact path of the attacker. |
| **Zero-Day Attacks** | Signature-based rules don't exist for new malware. | GNNs learn the *structural baseline* of the network, flagging any deviation. |
| **Insider Threats** | Insiders use valid credentials, so they aren't blocked. | The model flags when valid users access unauthorized nodes. |
| **Alert Fatigue** | High false positives from isolated anomalies. | Graph context reduces false positives (e.g., a spike in traffic is normal if it matches a known pattern). |

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    ALLBEN-GNN-THREAT-DETECTOR                           │
│                    Graph Autoencoder Architecture                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────────────┐                                              │
│   │  GRAPH BUILDER       │                                              │
│   │  src/graph_builder.py│                                              │
│   │  ├─ Nodes (Users)    │                                              │
│   │  ├─ Nodes (Servers)  │                                              │
│   │  └─ Edges (Logins)   │                                              │
│   └──────────┬───────────┘                                              │
│              │                                                          │
│              ▼                                                          │
│   ┌──────────────────────┐                                              │
│   │  GNN AUTOENCODER     │                                              │
│   │  src/gnn_model.py    │                                              │
│   │  ├─ GCN Encoder      │                                              │
│   │  ├─ Inner Product    │                                              │
│   │  │  Decoder          │                                              │
│   │  └─ Reconstruction   │                                              │
│   │     Loss            │                                              │
│   └──────────┬───────────┘                                              │
│              │                                                          │
│              ▼                                                          │
│   ┌──────────────────────┐                                              │
│   │  ANOMALY SCORING     │                                              │
│   │  ├─ Calculate Error  │                                              │
│   │  ├─ Normalize 0-1    │                                              │
│   │  └─ Flag > 0.7       │                                              │
│   └──────────┬───────────┘                                              │
│              │                                                          │
│              ▼                                                          │
│   ┌──────────────────────┐                                              │
│   │  STREAMLIT UI        │                                              │
│   │  src/app.py          │                                              │
│   │  ├─ PyVis Graph      │                                              │
│   │  ├─ Red Nodes        │                                              │
│   │  └─ Table of Anomalies│                                             │
│   └──────────────────────┘                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
