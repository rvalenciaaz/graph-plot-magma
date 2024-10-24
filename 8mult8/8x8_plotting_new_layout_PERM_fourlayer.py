import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import Arc
import math
import pickle
import numpy as np
import itertools
import random  # Import random for random sampling

def plot_graph_from_multiplication_table(M, table_index, num_permutations=100):
    n = len(M)  # Number of nodes, should be 8 after modification
    edges = set()  # Use a set to avoid duplicate edges

    # Construct edges based on the multiplication table
    for i in range(n):
        for j in range(n):
            k = M[i][j]  # Compute i * j
            edges.add((i, k))
            edges.add((k, j))

    # Create a DiGraph since we don't need multiple edges between nodes
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Save the graph to a file using pickle
    graph_filename = f'graph_{table_index}_reordered_nodes.pkl'
    with open(graph_filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph {table_index} data saved as '{graph_filename}'.")

    # Generate permutations of all 8 nodes
    all_nodes = list(G.nodes())
    total_permutations = math.factorial(len(all_nodes))
    if total_permutations <= num_permutations:
        permutations = list(itertools.permutations(all_nodes))
    else:
        # Randomly sample permutations
        permutations = [random.sample(all_nodes, len(all_nodes)) for _ in range(num_permutations)]

    for perm_index, permuted_nodes in enumerate(permutations, 1):
        pos = {}

        # Assign positions based on the permutation
        y_levels = [1, 0.5, 0, -0.5]  # The four y-levels
        idx = 0  # Index to track position in permuted_nodes
        for y in y_levels:
            nodes_in_level = permuted_nodes[idx:idx+2]  # Get the next 2 nodes
            x_coords = np.linspace(-1, 1, len(nodes_in_level)) if nodes_in_level else []
            for x_idx, node in enumerate(nodes_in_level):
                pos[node] = (x_coords[x_idx], y)
            idx += 2  # Move to the next pair

        # Draw nodes with labels
        plt.figure(figsize=(8, 6))  # Create a new figure for each permutation
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
        image_filename = f'graph_{table_index}_perm_4layer_{perm_index}_8x8_reordered_nodes.png'
        plt.savefig(image_filename, format='png',
                    bbox_inches='tight', pad_inches=0.1, dpi=100)
        plt.close()
        print(f"Graph {table_index} permutation {perm_index} plotted and saved as '{image_filename}'.")

        # Optional: Limit the number of permutations
        if perm_index >= num_permutations:
            break

    print(f"{perm_index} permutations plotted for graph {table_index}.")

def main():
    # File containing multiplication tables (one per row in list format)
    filename = 'magmas8x8(WIP).txt'

    # Desired graph indices (line numbers in the file)
    desired_graph_indices = [1, 2, 6, 512, 513, 516, 518, 1536]

    # Number of permutations to plot for each graph
    num_permutations = 100  # Adjust this number as needed

    # Read and process only the desired multiplication tables
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            if line_number in desired_graph_indices:
                try:
                    # Safely evaluate the line as a Python literal (list of lists)
                    M = ast.literal_eval(line.strip())
                    # Validate that M is a list of lists and is square
                    if (isinstance(M, list) and all(isinstance(row, list) for row in M)):
                        n = len(M)
                        if n == 8 and all(len(row) == n for row in M):
                            plot_graph_from_multiplication_table(M, line_number, num_permutations)
                        else:
                            print(f"Error on line {line_number}: The table must be 8x8.")
                    else:
                        print(f"Error on line {line_number}: The line is not a list of lists.")
                except (SyntaxError, ValueError) as e:
                    print(f"Error on line {line_number}: {e}")

if __name__ == '__main__':
    main()