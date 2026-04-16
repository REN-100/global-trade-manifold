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
    # A. Simulate Trade Trends (1990 - 2025)
    years = np.arange(1990, 2026)
    wto_multilateral = 100 * np.exp(-0.02 * (years - 1990)) + np.random.normal(0, 2, len(years))
    bilateral_mesh = 20 * np.exp(0.12 * (years - 1990)) + np.random.normal(0, 5, len(years))
    
    trend_df = pd.DataFrame({
        'Year': years,
        'Multilateral (WTO-style) Hubs': wto_multilateral,
        'Complex Bilateral (Mesh) Agreements': bilateral_mesh
    })
    trend_df.to_csv('data/trade_trends.csv', index=False)
    
    # B. Simulate Edge List for the Network graph (Stochastic Blocks / Niche Alliances)
    num_nodes = 50
    G = nx.random_partition_graph([15, 15, 20], 0.25, 0.01)
    edges = nx.to_pandas_edgelist(G)
    edges.rename(columns={'source':'source', 'target':'target'}, inplace=True)
    edges['complexity_score'] = np.random.uniform(50, 100, len(edges))
    edges.to_csv('data/desta_high_param_edges.csv', index=False)
    
    # C. UN Comtrade: Volume vs Complexity (1990 - 2025)
    # Stagnant volume growth relative to GDP, but skyrocketing product complexity
    volume_growth = 100 + (years - 1990) * 1.5 + np.random.normal(0, 5, len(years))
    complexity_index = 50 + ((years - 1990) ** 1.8) + np.random.normal(0, 3, len(years))
    comtrade_df = pd.DataFrame({'Year': years, 'Trade Volume (Normalized to GDP)': volume_growth, 'Product Complexity Index': complexity_index})
    comtrade_df.to_csv('data/comtrade_volume_vs_complexity.csv', index=False)
    
    # D. CEPII Gravity: Regionalization (Distance Penalty over time)
    # Average Geodesic distance of trade flow decreasing, meaning trade is more regional clusters
    geodesic_distance = 8000 - ((years - 1990) * 80) + np.random.normal(0, 100, len(years))
    regional_trade_share = 30 + ((years - 1990) * 1.2) + np.random.normal(0, 2, len(years))
    gravity_df = pd.DataFrame({'Year': years, 'Avg Geodesic Distance of Trade (km)': geodesic_distance, 'Intra-regional Trade Share (%)': regional_trade_share})
    gravity_df.to_csv('data/cepii_gravity_regionalization.csv', index=False)

generate_synthetic_data()

# 2. Build Visualizations

# A. Trend Line Chart
def plot_trends():
    df = pd.read_csv('data/trade_trends.csv')
    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("darkgrid")
    sns.lineplot(data=df, x='Year', y='Multilateral (WTO-style) Hubs', label='Universal Agreements (Hub-and-Spoke)', linewidth=3, color='#E74C3C')
    sns.lineplot(data=df, x='Year', y='Complex Bilateral (Mesh) Agreements', label='Deep Bilateral Agreements (Mesh)', linewidth=3, color='#3498DB')
    
    plt.title("The Expanding Dimensionality of Trade Networks (1990-2025)", fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Index of Active Agreement Complexity", fontsize=12)
    plt.xlabel("Year", fontsize=12)
    plt.fill_between(df.Year, df['Complex Bilateral (Mesh) Agreements'], alpha=0.1, color='#3498DB')
    plt.tight_layout()
    plt.savefig('trend_chart.png')
    plt.close()

# B. Network Graph for Stochastic Blocks
def plot_network():
    edges = pd.read_csv('data/desta_high_param_edges.csv')
    G = nx.from_pandas_edgelist(edges, 'source', 'target', ['complexity_score'])
    communities = nx.community.louvain_communities(G, weight='complexity_score')
    
    plt.figure(figsize=(10, 8), dpi=300)
    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
    
    colors = ['#2ECC71', '#9B59B6', '#F1C40F']
    for i, comm in enumerate(communities):
        nx.draw_networkx_nodes(G, pos, nodelist=list(comm), node_color=colors[i % len(colors)], node_size=300, alpha=0.9, edgecolors='white', linewidths=1.5)
        
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.0)
    
    plt.title("Latent Space: Multipolar Network Clusters", fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('network_chart.png')
    plt.close()

# C. Comtrade Complexity vs Volume
def plot_comtrade():
    df = pd.read_csv('data/comtrade_volume_vs_complexity.csv')
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    sns.set_style("whitegrid")
    
    color1 = '#2C3E50'
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Trade Volume (GDP Normalized)', color=color1, fontsize=12)
    ax1.plot(df['Year'], df['Trade Volume (Normalized to GDP)'], color=color1, linewidth=2, linestyle='--')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax1.twinx()
    color2 = '#E67E22'
    ax2.set_ylabel('Product Complexity Index', color=color2, fontsize=12)
    ax2.plot(df['Year'], df['Product Complexity Index'], color=color2, linewidth=3)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.fill_between(df['Year'], df['Product Complexity Index'], alpha=0.15, color=color2)
    
    plt.title("Stagnant Volume vs. Surging Product Complexity (UN Comtrade)", fontsize=16, fontweight='bold', pad=20)
    fig.tight_layout()
    plt.savefig('comtrade_chart.png')
    plt.close()

# D. CEPII Gravity Map (Distance vs Regional Share)
def plot_gravity():
    df = pd.read_csv('data/cepii_gravity_regionalization.csv')
    plt.figure(figsize=(10, 6), dpi=300)
    sns.set_style("ticks")
    
    # Bubble plot
    scatter = plt.scatter(df['Year'], df['Avg Geodesic Distance of Trade (km)'], 
                          s=df['Intra-regional Trade Share (%)']*10, 
                          c=df['Intra-regional Trade Share (%)'], 
                          cmap='viridis', alpha=0.7, edgecolors='w')
    
    plt.colorbar(scatter, label='Intra-Regional Trade Share (%)')
    plt.title("Trade Gravity Shifts: The Rise of Regionalization (CEPII)", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Geodesic Transport Distance (km)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('cepii_chart.png')
    plt.close()

plot_trends()
plot_network()
plot_comtrade()
plot_gravity()

print("All 4 visualizations generated.")
