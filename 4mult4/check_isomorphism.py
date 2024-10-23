import networkx as nx
import pickle
from itertools import combinations
import csv

def load_graphs(num_graphs):
    """
    Loads saved graphs from pickle files.

    Parameters:
    - num_graphs: The number of graphs to load.

    Returns:
    - A list of tuples containing the graph index and the graph object.
    """
    graphs = []
    for index in range(1, num_graphs + 1):
        filename = f'graph_{index}.pkl'
        with open(filename, 'rb') as f:
            G = pickle.load(f)
        graphs.append((index, G))
        print(f"Graph {index} loaded.")
    return graphs

def check_isomorphism(graphs):
    """
    Checks pairwise isomorphism between graphs.

    Parameters:
    - graphs: A list of tuples containing graph indices and graph objects.

    Returns:
    - A list of dictionaries representing the melted table.
    """
    melted_table = []
    for (i, G1), (j, G2) in combinations(graphs, 2):
        # Define node and edge match functions
        nm = lambda n1, n2: True  # Assuming nodes have no attributes to compare
        em = lambda e1, e2: e1 == e2  # Compare edge data dictionaries
        # Use MultiDiGraphMatcher with custom edge_match
        matcher = nx.algorithms.isomorphism.MultiDiGraphMatcher(G1, G2, node_match=nm, edge_match=em)
        is_iso = matcher.is_isomorphic()
        # Append result to the melted table
        melted_table.append({
            'Graph1': i,
            'Graph2': j,
            'Isomorphic': 'Yes' if is_iso else 'No'
        })
    return melted_table

def save_melted_table(melted_table, filename):
    """
    Saves the melted table to a CSV file.

    Parameters:
    - melted_table: The list of dictionaries representing the melted table.
    - filename: The name of the output CSV file.
    """
    fieldnames = ['Graph1', 'Graph2', 'Isomorphic']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in melted_table:
            writer.writerow(row)
    print(f"Melted table saved to '{filename}'.")

def main():
    # Specify the number of graphs you have saved
    num_graphs = 24 # Replace with the actual number of graphs
    # Load the graphs
    graphs = load_graphs(num_graphs)
    # Check for isomorphism pairwise and get the melted table data
    melted_table = check_isomorphism(graphs)
    # Save the melted table to a file
    output_filename = 'isomorphism_results.csv'
    save_melted_table(melted_table, output_filename)
    # Optionally, print the results
    print("\nIsomorphism Results:")
    for row in melted_table:
        print(f"Graphs {row['Graph1']} and {row['Graph2']}: {row['Isomorphic']}")

if __name__ == '__main__':
    main()
