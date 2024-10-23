import networkx as nx
import pickle

# Function to load a graph from a pickle file
def load_graph(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# File paths to the graph files
file_paths = [
    "graph_1_4x4.pkl",  # Replace with the actual path
    "graph_1536_8x8.pkl",  # Replace with the actual path
    "graph_4_4x4.pkl"   # Replace with the actual path
]

# Load the graphs
graph_1_4x4 = load_graph(file_paths[0])
graph_1_8x8 = load_graph(file_paths[1])
graph_4_4x4 = load_graph(file_paths[2])

# Check if each 4x4 graph is a subgraph of the 8x8 graph
gm1 = nx.isomorphism.GraphMatcher(graph_1_8x8, graph_1_4x4)
gm2 = nx.isomorphism.GraphMatcher(graph_1_8x8, graph_4_4x4)

subgraph_1_4x4_in_8x8 = gm1.subgraph_is_isomorphic()
subgraph_4_4x4_in_8x8 = gm2.subgraph_is_isomorphic()

# Output the results
print(f"Is graph_1_4x4 a subgraph of graph_1_8x8? {subgraph_1_4x4_in_8x8}")
print(f"Is graph_4_4x4 a subgraph of graph_1_8x8? {subgraph_4_4x4_in_8x8}")
