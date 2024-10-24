import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Arc
import math
import pickle
import numpy as np
import itertools
from networkx.algorithms import isomorphism

def load_subgraph(subgraph_filename):
    """Load the subgraph from a pickle file."""
    with open(subgraph_filename, 'rb') as f:
        subgraph = pickle.load(f)
    return subgraph

def plot_graph_from_multiplication_table(M, table_index, subgraph):
    n = len(M)  # Number of nodes, should be 8
    edges = set()  # Use a set to avoid duplicate edges

    # Construct edges based on the multiplication table
    for i in range(n):
        for j in range(n):
            k = M[i][j]
            edges.add((i, k))
            edges.add((k, j))

    # Create a DiGraph
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Save the graph to a file using pickle
    graph_filename = f'graph_{table_index}_reordered_nodes.pkl'
    with open(graph_filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph {table_index} data saved as '{graph_filename}'.")

    # Check for subgraph isomorphism, including self-loops
    GM = isomorphism.DiGraphMatcher(G, subgraph)
    subgraph_found = GM.subgraph_is_isomorphic()

    if subgraph_found:
        # Get the mapping and edges of the subgraph within G
        mapping = next(GM.subgraph_isomorphisms_iter())
        # Map subgraph edges to corresponding edges in G
        subgraph_edges_in_G = set((mapping[u], mapping[v]) for u, v in subgraph.edges())
        print(f"Subgraph found in graph {table_index}. Highlighting subgraph edges.")
    else:
        subgraph_edges_in_G = set()
        print(f"Subgraph not found in graph {table_index}.")

    # Compute total degrees
    total_degrees = {node: G.in_degree(node) + G.out_degree(node) for node in G.nodes()}

    # Partition nodes based on total degree
    nodes_degree_8 = [node for node, deg in total_degrees.items() if deg == 8]
    nodes_degree_4 = [node for node, deg in total_degrees.items() if deg == 4]
    nodes_other = [node for node in G.nodes() if node not in nodes_degree_8 and node not in nodes_degree_4]

    # Generate all permutations of the top nodes
    permutations = list(itertools.permutations(nodes_degree_8))

    for perm_index, permuted_top_nodes in enumerate(permutations, 1):
        pos = {}

        # Arrange permuted top nodes at the top (y=1)
        x_coords_8 = np.linspace(-1, 1, len(permuted_top_nodes)) if permuted_top_nodes else []
        for idx, node in enumerate(permuted_top_nodes):
            pos[node] = (x_coords_8[idx], 1)

        # Arrange nodes with total degree 4 at the bottom (y=-1)
        x_coords_4 = np.linspace(-1, 1, len(nodes_degree_4)) if nodes_degree_4 else []
        for idx, node in enumerate(nodes_degree_4):
            pos[node] = (x_coords_4[idx], -1)

        # Arrange other nodes at y=0
        if nodes_other:
            x_coords_other = np.linspace(-1, 1, len(nodes_other))
            for idx, node in enumerate(nodes_other):
                pos[node] = (x_coords_other[idx], 0)

        # Draw nodes with labels
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue',
                               edgecolors='black', linewidths=1.5)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        ax = plt.gca()
        drawn_edges = set()

        # Iterate over all edges to draw them
        for u, v in G.edges():
            if (u, v) in drawn_edges:
                continue

            # Determine if the edge is part of the subgraph
            is_subgraph_edge = (u, v) in subgraph_edges_in_G

            # Set default edge properties
            if u == v:
                # Self-loop
                edge_color = 'green'
                if is_subgraph_edge:
                    edge_color = 'lightblue'
                x, y = pos[u]
                radius = 0.1
                arc = Arc((x, y), radius * 2, radius * 2, angle=0,
                          theta1=0, theta2=360,
                          color=edge_color, lw=1)
                ax.add_patch(arc)
                # Arrowhead
                arrow_angle = 45
                arrow_x = x + radius * math.cos(math.radians(arrow_angle))
                arrow_y = y + radius * math.sin(math.radians(arrow_angle))
                ax.annotate("",
                            xy=(arrow_x, arrow_y),
                            xytext=(x, y),
                            arrowprops=dict(arrowstyle="->", color=edge_color, lw=1, mutation_scale=15))
                drawn_edges.add((u, v))
            elif G.has_edge(v, u) and (v, u) not in drawn_edges:
                # Bidirectional edge
                edge_color_uv = 'red'
                edge_color_vu = 'red'
                if is_subgraph_edge:
                    edge_color_uv = 'lightblue'
                if (v, u) in subgraph_edges_in_G:
                    edge_color_vu = 'lightblue'
                nx.draw_networkx_edges(G, pos,
                                       edgelist=[(u, v)],
                                       arrowstyle='-|>',
                                       arrowsize=20,
                                       edge_color=edge_color_uv,
                                       connectionstyle="arc3,rad=-0.1",
                                       min_source_margin=15,
                                       min_target_margin=15)
                nx.draw_networkx_edges(G, pos,
                                       edgelist=[(v, u)],
                                       arrowstyle='-|>',
                                       arrowsize=20,
                                       edge_color=edge_color_vu,
                                       connectionstyle="arc3,rad=0.1",
                                       min_source_margin=15,
                                       min_target_margin=15)
                drawn_edges.add((u, v))
                drawn_edges.add((v, u))
            else:
                # Unidirectional edge
                edge_color = 'black'
                if is_subgraph_edge:
                    edge_color = 'lightblue'
                nx.draw_networkx_edges(G, pos,
                                       edgelist=[(u, v)],
                                       arrowstyle='-|>',
                                       arrowsize=20,
                                       edge_color=edge_color,
                                       connectionstyle="arc3,rad=0.05",
                                       min_source_margin=15,
                                       min_target_margin=15)
                drawn_edges.add((u, v))

        # Remove axes and adjust layout
        plt.axis('off')
        plt.tight_layout()

        # Save the graph image to a file
        image_filename = f'graph_{table_index}_permutation_{perm_index}_8x8_reordered_nodes_subg.png'
        plt.savefig(image_filename, format='png',
                    bbox_inches='tight', pad_inches=0.1, dpi=100)
        plt.close()
        print(f"Graph {table_index} permutation {perm_index} plotted and saved as '{image_filename}'.")

    print(f"All {len(permutations)} permutations plotted for graph {table_index}.")

def main():
    # File containing multiplication tables (one per line in list format)
    filename = 'magmas8x8(WIP).txt'

    # Desired graph indices (line numbers in the file)
    desired_graph_indices = [1, 2, 6, 512, 513, 516, 518, 1536]

    # Load the subgraph from a pickle file
    subgraph_filename = 'subgraph.pkl'  # Replace with your subgraph filename
    subgraph = load_subgraph(subgraph_filename)

    # Read and process only the desired multiplication tables
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            if line_number in desired_graph_indices:
                try:
                    # Safely evaluate the line as a Python literal
                    M = ast.literal_eval(line.strip())
                    # Validate that M is a square 8x8 table
                    if (isinstance(M, list) and all(isinstance(row, list) for row in M) and
                        len(M) == 8 and all(len(row) == 8 for row in M)):
                        plot_graph_from_multiplication_table(M, line_number, subgraph)
                    else:
                        print(f"Error on line {line_number}: The table must be 8x8.")
                except (SyntaxError, ValueError) as e:
                    print(f"Error on line {line_number}: {e}")

if __name__ == '__main__':
    main()
