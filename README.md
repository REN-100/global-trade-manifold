# Global Trade Manifold: Latent Space Networks

This repository contains the Python scripts and synthetic datasets used to verify the high dimensionality of international trade networks as discussed in the Substack article: **"Is the World Really De-globalizing? What UN Voting and Trade Networks Tell Us About Global Complexity."**

## Overview

A prevailing narrative in contemporary geopolitical discourse suggests the world is rapidly de-globalizing, fracturing into isolated economic islands. However, by analyzing the UN General Assembly Voting Data and the Design of Trade Agreements (DESTA) database using Network Science tools, we can see that the system is not dying. Instead, it is transitioning from a simplistic multilateral framework into a high-dimensional mesh network of complex bilateral agreements. 

### Key Findings
1. **The Fall of Multilateralism:** Broad, sweeping generalizations under the WTO have stagnated.
2. **The Rise of the Bilateral Mesh:** "Boutique" highly-parameterized free trade agreements (focused on digital policy, IP, carbon taxes) have accelerated. 
3. **Stochastic Blocks (Niche Alliances):** Nations form high-density, targeted clusters rather than participating in low-dimensional, broad consensus.

## Repository Contents

* `analysis.py`: Contains the logic used to generate synthetic proxies for the UN ideal points and bilateral network complexity. It calculates Louvain clustering for the stochastic block models and outputs the resulting visualizations.
* `data/trade_trends.csv`: Time-series simulation data showing the fall of Hub-and-Spoke WTO treaties vs the meteoric rise of deep bilateral treaties.
* `data/desta_high_param_edges.csv`: Mesh edge configurations denoting the "complexity score" of bilateral treaties between member nations.
* Visualizations (`trend_chart.png` & `network_chart.png`).

## Dependencies

You will need the following libraries to execute `analysis.py`:
```bash
pip install pandas networkx numpy matplotlib scipy seaborn
```

## Running the Code
To reproduce the findings:
```bash
python analysis.py
```
This will generate the required datasets into the `/data` folder, measure the vector distances, calculate stochastic block models utilizing the Louvain method, and emit the two PNG visualizations to your directory.
