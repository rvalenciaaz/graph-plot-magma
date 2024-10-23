import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pickle

# Adjacency matrix provided by the user with self-loops
adj_matrix = np.array([
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Create a directed graph from the adjacency matrix
G_self_loop = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)

# Plot the new graph with self-loops using a circular layout and order the nodes counter-clockwise by node name
plt.figure(figsize=(8, 8))

# Generate circular layout
pos = nx.circular_layout(G_self_loop)

# Sort nodes counter-clockwise by node name
sorted_nodes = sorted(G_self_loop.nodes())

# Create a mapping of positions to the sorted nodes
pos_sorted = {node: pos[node] for node in sorted_nodes}

# Draw the graph with the sorted layout
nx.draw(G_self_loop, pos_sorted, with_labels=True, node_color='skyblue', node_size=700, arrowstyle='->', arrowsize=15)
plt.title('Directed Graph with Self-Loops (Circular Layout)')

# Save the plot with circular layout and sorted nodes
circular_plot_filename = 'directed_graph_circular_sorted.png'
plt.savefig(circular_plot_filename)

# Save the NetworkX graph object as a pickle file
pickle_graph_filename = 'graph_order_16.pkl'
with open(pickle_graph_filename, 'wb') as f:
    pickle.dump(G_self_loop, f)

# Print the paths for saved files
print(f"Graph plot saved as: {circular_plot_filename}")
print(f"Graph object saved as: {pickle_graph_filename}")
