import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset (Replace this with the actual path to your file)
file_path = 'isomorphism_results.csv'
df = pd.read_csv(file_path)

# Filter the dataset for isomorphic pairs
isomorphic_pairs = df[df['Isomorphic'] == 'Yes']

# Create the graph
G = nx.Graph()

# Add edges for each isomorphic pair
for _, row in isomorphic_pairs.iterrows():
    G.add_edge(row['Graph1'], row['Graph2'])

# **New code to save a representative from each connected subgraph**
# Get connected components
components = list(nx.connected_components(G))

# For each component, pick a representative node
representatives = [next(iter(comp)) for comp in components]

# Save the representatives to a file
with open('representative_graphs.txt', 'w') as f:
    for rep in representatives:
        f.write(f"{rep}\n")

# Define the size of the plot
plt.figure(figsize=(10, 10), dpi=600)

# Draw the graph with custom node and edge styles
# Increase spacing between nodes using the 'k' parameter to make them more sparse
pos = nx.spring_layout(G, seed=42, k=0.5)
nx.draw_networkx_nodes(G, pos, node_size=800, node_color="skyblue", edgecolors="black")
nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=12, font_color="black", font_weight="bold")

# Add representative labels (node numbers) near the connected components
for i, rep_node in enumerate(representatives):
    x, y = pos[rep_node]
    plt.text(x, y + 0.05, f"Rep {i+1} (Node {rep_node})", fontsize=10, fontweight="bold", color="red")

# Add a title and remove the axes for a cleaner look
plt.title("Isomorphic Graph Network", size=15, weight='bold')
plt.axis("off")

# Save the plot to a file
plt.savefig("isomorphism_graph_plot_8x8.png", dpi=600)
plt.show()