import networkx as nx
import pickle
import matplotlib.pyplot as plt
from itertools import product

# Function to load the graph from a pickle file
def load_graph_from_pkl(filename):
    with open(filename, 'rb') as f:
        graph = pickle.load(f)
    return graph

# Function to compute the direct (tensor) product of two graphs
def compute_direct_product(graph1, graph2):
    return nx.tensor_product(graph1, graph2)

# Function to check if a graph is a subgraph of another graph
def is_subgraph(subgraph, graph):
    return nx.algorithms.isomorphism.GraphMatcher(graph, subgraph).subgraph_is_isomorphic()

# Function to plot a graph
def plot_graph(graph, title="Graph"):
    pos = nx.spring_layout(graph)  # Positions for all nodes
    plt.figure(figsize=(8, 8))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.title(title)
    plt.show()

# Function to test all combinations of products
def test_all_product_combinations(graphs, subgraph):
    # Get all pairwise combinations of the graphs (including itself)
    for i, (g1, g2) in enumerate(product(graphs, repeat=2), 1):
        # Compute the direct product
        direct_product_graph = compute_direct_product(g1, g2)

        # Plot the direct product graph
        plot_title = f"Direct Product Graph {i}: G{graphs.index(g1)+1} x G{graphs.index(g2)+1}"
        plot_graph(direct_product_graph, title=plot_title)

        # Check if the subgraph is a subgraph of the direct product
        if is_subgraph(subgraph, direct_product_graph):
            print(f"{plot_title}: The third graph is a subgraph.")
        else:
            print(f"{plot_title}: The third graph is NOT a subgraph.")

# Main function to load the graphs, compute the products, and check for subgraphs
def main():
    # Replace these with your actual pkl filenames
    graph_files = ['graph_1_4x4.pkl', 'graph_4_4x4.pkl']  # Add more graph filenames as needed
    subgraph_file = 'graph_512_8x8.pkl'  # Third graph to check if it's a subgraph

    # Load the graphs
    graphs = [load_graph_from_pkl(file) for file in graph_files]
    subgraph = load_graph_from_pkl(subgraph_file)

    # Test all product combinations and check for subgraph
    test_all_product_combinations(graphs, subgraph)

if __name__ == "__main__":
    main()