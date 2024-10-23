import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Arc
import math
import pickle
import numpy as np  # Import numpy for linspace

def plot_graph_from_multiplication_table(M, table_index):
    n = len(M)  # Number of nodes, should be 8 after modification
    edges = set()  # Use a set to avoid duplicate edges

    # Construct edges based on the multiplication table
    for i in range(n):
        for j in range(n):
            k = M[i][j]  # Compute i * j
            edges.add((i, k))
            edges.add((k, j))
    #print(f"Edges for graph {table_index}: {edges}")

    # Create a DiGraph since we don't need multiple edges between nodes
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Save the graph to a file using pickle
    graph_filename = f'graph_{table_index}_reordered_nodes.pkl'
    with open(graph_filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph {table_index} data saved as '{graph_filename}'.")

    # Compute total degrees
    total_degrees = {node: G.in_degree(node) + G.out_degree(node) for node in G.nodes()}

    # Partition nodes based on total degree
    nodes_degree_8 = [node for node, deg in total_degrees.items() if deg == 8]
    nodes_degree_4 = [node for node, deg in total_degrees.items() if deg == 4]
    nodes_other = [node for node in G.nodes() if node not in nodes_degree_8 and node not in nodes_degree_4]

    # Define positions for nodes
    pos = {}

    # Arrange nodes with total degree 8 at the top (y=1)
    x_coords_8 = np.linspace(-1, 1, len(nodes_degree_8)) if nodes_degree_8 else []
    for idx, node in enumerate(nodes_degree_8):
        pos[node] = (x_coords_8[idx], 1)

    # Arrange nodes with total degree 4 at the bottom (y=-1)
    x_coords_4 = np.linspace(-1, 1, len(nodes_degree_4)) if nodes_degree_4 else []
    for idx, node in enumerate(nodes_degree_4):
        pos[node] = (x_coords_4[idx], -1)

    # If there are nodes with other degrees, arrange them at y=0
    if nodes_other:
        x_coords_other = np.linspace(-1, 1, len(nodes_other))
        for idx, node in enumerate(nodes_other):
            pos[node] = (x_coords_other[idx], 0)

    # Draw nodes with labels
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue',
                           edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    ax = plt.gca()

    # Prepare a set to keep track of drawn edges
    drawn_edges = set()

    # Iterate over all edges to draw them
    for u, v in G.edges():
        # Avoid drawing the same edge multiple times
        if (u, v) in drawn_edges:
            continue

        # First, handle self-loops
        if u == v:
            # Draw self-loop using Arc
            x, y = pos[u]
            radius = 0.1  # Adjust the radius of the self-loop
            theta1 = 0
            theta2 = 360  # Full circle
            # Create an Arc object
            arc = Arc((x, y), radius * 2, radius * 2, angle=0,
                      theta1=theta1, theta2=theta2,
                      color='green', lw=1)
            ax.add_patch(arc)

            # Optionally, add an arrowhead manually
            # Calculate the position for the arrowhead
            arrow_angle = 45  # degrees
            arrow_x = x + radius * math.cos(math.radians(arrow_angle))
            arrow_y = y + radius * math.sin(math.radians(arrow_angle))
            ax.annotate("",
                        xy=(arrow_x, arrow_y),
                        xytext=(x, y),
                        arrowprops=dict(arrowstyle="->", color='black', lw=1))
            # Mark edge as drawn
            drawn_edges.add((u, v))

        # Then, check for bidirectional edges
        elif G.has_edge(v, u) and (v, u) not in drawn_edges:
            # Bidirectional edge
            # Edge from u to v
            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(u, v)],
                                   arrowstyle='-|>',
                                   arrowsize=10,
                                   edge_color='red',
                                   connectionstyle="arc3,rad=-0.1",
                                   min_source_margin=15,
                                   min_target_margin=15)
            # Edge from v to u
            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(v, u)],
                                   arrowstyle='-|>',
                                   arrowsize=10,
                                   edge_color='red',
                                   connectionstyle="arc3,rad=0.1",
                                   min_source_margin=15,
                                   min_target_margin=15)
            # Mark both edges as drawn
            drawn_edges.add((u, v))
            drawn_edges.add((v, u))
        else:
            # Unidirectional edge
            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(u, v)],
                                   arrowstyle='-|>',
                                   arrowsize=10,
                                   edge_color='black',
                                   connectionstyle="arc3,rad=0.05",
                                   min_source_margin=15,
                                   min_target_margin=15)
            # Mark edge as drawn
            drawn_edges.add((u, v))

    # Remove axes for clarity
    plt.axis('off')

    # Adjust plot margins
    plt.tight_layout()

    # Save the graph image to a file
    image_filename = f'graph_{table_index}_8x8_reordered_nodes.png'
    plt.savefig(image_filename, format='png',
                bbox_inches='tight', pad_inches=0.1, dpi=100)
    plt.close()
    print(f"Graph {table_index} plotted and saved as '{image_filename}'.")


def read_multiplication_tables_from_file(filename):
    multiplication_tables = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            try:
                # Safely evaluate the line as a Python literal (list of lists)
                M = ast.literal_eval(line.strip())
                # Validate that M is a list of lists and is square
                if (isinstance(M, list) and all(isinstance(row, list) for row in M)):
                    n = len(M)
                    if n == 8 and all(len(row) == n for row in M):
                        multiplication_tables.append(M)
                    else:
                        print(f"Error on line {line_number}: The table must be 8x8.")
                else:
                    print(f"Error on line {line_number}: The line is not a list of lists.")
            except (SyntaxError, ValueError) as e:
                print(f"Error on line {line_number}: {e}")
    return multiplication_tables

def main():
    # File containing multiplication tables (one per row in list format)
    filename = 'magmas8x8(WIP).txt'

    # Read multiplication tables from the file
    multiplication_tables = read_multiplication_tables_from_file(filename)

    # Plot each multiplication table and save graphs to files
    for index, M in enumerate(multiplication_tables, 1):
        plot_graph_from_multiplication_table(M, index)

if __name__ == '__main__':
    main()
