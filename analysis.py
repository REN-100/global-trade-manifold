import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
import os

# Create mock data directory
os.makedirs('data', exist_ok=True)

# 1. Generate Synthetic Data for the visualizations
def generate_synthetic_data():
    # Simulate Trade Trends (1990 - 2025)
    years = np.arange(1990, 2026)
    wto_multilateral = 100 * np.exp(-0.02 * (years - 1990)) + np.random.normal(0, 2, len(years))
    bilateral_mesh = 20 * np.exp(0.12 * (years - 1990)) + np.random.normal(0, 5, len(years))
    
    trend_df = pd.DataFrame({
        'Year': years,
        'Multilateral (WTO-style) Hubs': wto_multilateral,
        'Complex Bilateral (Mesh) Agreements': bilateral_mesh
    })
    trend_df.to_csv('data/trade_trends.csv', index=False)
    
    # Simulate Edge List for the Network graph (Stochastic Blocks / Niche Alliances)
    num_nodes = 50
    G = nx.random_partition_graph([15, 15, 20], 0.25, 0.01)
    # create edges list
    edges = nx.to_pandas_edgelist(G)
    edges.rename(columns={'source':'source', 'target':'target'}, inplace=True)
    edges['complexity_score'] = np.random.uniform(50, 100, len(edges))
    edges.to_csv('data/desta_high_param_edges.csv', index=False)

generate_synthetic_data()

# 2. Build Visualizations

# A. Trend Line Chart
def plot_trends():
    df = pd.read_csv('data/trade_trends.csv')
    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("darkgrid")
    sns.lineplot(data=df, x='Year', y='Multilateral (WTO-style) Hubs', label='Universal/Multilateral Agreements (Hub-and-Spoke)', linewidth=3, color='#E74C3C')
    sns.lineplot(data=df, x='Year', y='Complex Bilateral (Mesh) Agreements', label='Deep Bilateral Agreements (Mesh/Niche)', linewidth=3, color='#3498DB')
    
    plt.title("The Expanding Dimensionality of Trade Networks (1990-2025)", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Index of Active Agreement Complexity", fontsize=12)
    plt.xlabel("Year", fontsize=12)
    plt.fill_between(df.Year, df['Complex Bilateral (Mesh) Agreements'], alpha=0.1, color='#3498DB')
    plt.annotate('Shift from Hub-and-Spoke to Mesh', xy=(2010, 250), xytext=(2000, 400),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
    plt.tight_layout()
    plt.savefig('trend_chart.png')
    plt.close()

# B. Network Graph for Stochastic Blocks
def plot_network():
    edges = pd.read_csv('data/desta_high_param_edges.csv')
    G = nx.from_pandas_edgelist(edges, 'source', 'target', ['complexity_score'])
    
    # Identify Niche Alliances via Stochastic Block clustering proxy (Louvain)
    # In networkx 3.x louvain is built-in
    communities = nx.community.louvain_communities(G, weight='complexity_score')
    
    plt.figure(figsize=(10, 8), dpi=300)
    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
    
    colors = ['#2ECC71', '#9B59B6', '#F1C40F']
    for i, comm in enumerate(communities):
        nx.draw_networkx_nodes(G, pos, nodelist=list(comm), node_color=colors[i % len(colors)], node_size=300, alpha=0.9, edgecolors='white', linewidths=1.5)
        
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.0)
    
    plt.title("Latent Space Visualization: Multipolar Network Clusters\n(Stochastic Block Distribution of Niche Alliances)", fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('network_chart.png')
    plt.close()

plot_trends()
plot_network()

print("Visualizations generated: trend_chart.png, network_chart.png")
