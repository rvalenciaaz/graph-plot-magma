import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'isomorphism_results.csv'  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Filter the dataset for isomorphic pairs
isomorphic_pairs = df[df['Isomorphic'] == 'Yes']

# Create the graph
G = nx.Graph()

# Add edges for each isomorphic pair
for _, row in isomorphic_pairs.iterrows():
    G.add_edge(row['Graph1'], row['Graph2'])

# Define the size of the plot
plt.figure(figsize=(10, 10), dpi=600)

# Draw the graph with custom node and edge styles
pos = nx.spring_layout(G, seed=42)  # Positions the nodes for a better layout
nx.draw_networkx_nodes(G, pos, node_size=800, node_color="skyblue", edgecolors="black")
nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=12, font_color="black", font_weight="bold")

# Add a title and remove the axes for a cleaner look
plt.title("Isomorphic Graph Network", size=15, weight='bold')
plt.axis("off")

# Show the plot
#plt.show()
plt.savefig("isomorphism_graph_plot_4x4.png",dpi=600)