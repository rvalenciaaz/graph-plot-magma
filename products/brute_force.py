import numpy as np
from itertools import permutations
from tqdm import tqdm

# Number of nodes
nodes = 8

# Required in-degrees and out-degrees
in_degrees = [4, 4, 4, 4, 2, 2, 2, 2]
out_degrees = [4, 4, 4, 4, 2, 2, 2, 2]

# Function to check if the degree constraints are satisfied
def satisfies_degrees(adjacency_matrix, in_degrees, out_degrees):
    in_degree_actual = np.sum(adjacency_matrix, axis=0)  # column sum for in-degrees
    out_degree_actual = np.sum(adjacency_matrix, axis=1)  # row sum for out-degrees
    return (np.array(in_degrees) == in_degree_actual).all() and (np.array(out_degrees) == out_degree_actual).all()

# Generate all potential edges (excluding self-loops)
all_nodes = range(nodes)
possible_edges = [(i, j) for i in all_nodes for j in all_nodes if i != j]

# Function to find all valid graphs
def find_all_possible_graphs():
    valid_graphs = []
    total_permutations = len(list(permutations(possible_edges, 24)))
    
    # Use tqdm to track progress
    for edge_selection in tqdm(permutations(possible_edges, 24), total=total_permutations):
        # Create an adjacency matrix
        adjacency_matrix = np.zeros((nodes, nodes), dtype=int)
        
        # Add edges to the adjacency matrix
        for edge in edge_selection:
            adjacency_matrix[edge[0], edge[1]] = 1
        
        # Check if the in-degree and out-degree constraints are satisfied
        if satisfies_degrees(adjacency_matrix, in_degrees, out_degrees):
            valid_graphs.append(adjacency_matrix)
    
    return valid_graphs

# Find all valid directed graphs
valid_graphs = find_all_possible_graphs()

# Output the number of valid graphs found
print(f"Number of valid directed graphs: {len(valid_graphs)}")
