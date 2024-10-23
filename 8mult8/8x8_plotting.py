import networkx as nx
import matplotlib.pyplot as plt
import ast
from matplotlib.patches import FancyArrowPatch
import math
import pickle  # Import the pickle module

def plot_graph_from_multiplication_table(M, table_index):
    """
    Constructs and plots a graph based on the given multiplication table M.
    Also saves the graph object to a file for later use.

    Parameters:
    - M: A list of lists representing the multiplication table.
         M[i][j] represents the result of i * j.
    - table_index: An integer representing the index of the multiplication table (used for saving plots and graph files).
    """
    n = len(M)  # Number of nodes, should be 8 as per your note
    edges = []

    # Construct edges based on the multiplication table
    for i in range(n):
        for j in range(n):
            k = M[i][j]  # Compute i * j
            edges.append((i, k))
            edges.append((k, j))

    # Create a MultiDiGraph to allow multiple edges between nodes
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Save the graph to a file using pickle
    graph_filename = f'graph_{table_index}.pkl'
    with open(graph_filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph {table_index} data saved as '{graph_filename}'.")

    # Define fixed positions for nodes from 0 to 7 counterclockwise
    pos = {}
    for i in range(n):
        angle = math.pi / 2 - (2 * math.pi * i) / n  # Start from pi/2 and go counterclockwise
        x = math.cos(angle)
        y = math.sin(angle)
        pos[i] = (x, y)

    # Draw nodes with labels
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

    ax = plt.gca()

    # Prepare a set to keep track of drawn edges
    drawn_edges = set()

    # Iterate over all edges to draw them
    for u, v in G.edges():
        # Avoid drawing the same edge multiple times
        if (u, v) in drawn_edges:
            continue

        # Check if there is a reverse edge (bidirectional)
        if G.has_edge(v, u) and (v, u) not in drawn_edges:
            # Bidirectional edge
            # Draw both edges as straight lines in red
            # Edge from u to v
            arrow = FancyArrowPatch(posA=pos[u], posB=pos[v],
                                    arrowstyle='-|>',
                                    mutation_scale=15,
                                    color='red',
                                    lw=1,
                                    connectionstyle="arc3,rad=0",
                                    shrinkA=15,
                                    shrinkB=15)
            ax.add_patch(arrow)

            # Edge from v to u
            arrow_rev = FancyArrowPatch(posA=pos[v], posB=pos[u],
                                        arrowstyle='-|>',
                                        mutation_scale=15,
                                        color='red',
                                        lw=1,
                                        connectionstyle="arc3,rad=0",
                                        shrinkA=15,
                                        shrinkB=15)
            ax.add_patch(arrow_rev)

            # Mark both edges as drawn
            drawn_edges.add((u, v))
            drawn_edges.add((v, u))
        else:
            # Unidirectional edge or self-loop
            if u == v:
                # Self-loop as a bent edge
                rad = 0.3  # Curvature radius for self-loops
                arrow = FancyArrowPatch(posA=pos[u], posB=pos[v],
                                        arrowstyle='-|>',
                                        mutation_scale=15,
                                        color='black',
                                        lw=1,
                                        connectionstyle=f"arc3,rad={rad}",
                                        shrinkA=15,
                                        shrinkB=15)
                ax.add_patch(arrow)
            else:
                # Unidirectional edge
                arrow = FancyArrowPatch(posA=pos[u], posB=pos[v],
                                        arrowstyle='-|>',
                                        mutation_scale=15,
                                        color='black',
                                        lw=1,
                                        connectionstyle="arc3,rad=0",
                                        shrinkA=15,
                                        shrinkB=15)
                ax.add_patch(arrow)

            # Mark edge as drawn
            drawn_edges.add((u, v))

    # Remove axes for clarity
    plt.axis('off')

    # Adjust plot margins
    plt.tight_layout()

    # Save the graph image to a file
    image_filename = f'graph_{table_index}_8x8.png'
    plt.savefig(image_filename, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()
    print(f"Graph {table_index} plotted and saved as '{image_filename}'.")

def read_multiplication_tables_from_file(filename):
    """
    Reads multiplication tables from a file, one per row, where each table is in list format.

    Parameters:
    - filename: The name of the file containing multiplication tables.

    Returns:
    - A list of multiplication tables, where each table is a list of lists.
    """
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
