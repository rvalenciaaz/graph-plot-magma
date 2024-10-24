import networkx as nx
import pickle

def reconstruct_multiplication_table_from_graph(graph_filename, n):
    """
    Reconstructs the multiplication table M from the graph stored in 'graph_filename'.

    Parameters:
    - graph_filename: The filename of the graph saved as a pickle file.
    - n: The number of nodes in the graph (size of the multiplication table).

    Returns:
    - M: The reconstructed multiplication table as a list of lists.
    """
    # Load the graph from the pickle file
    with open(graph_filename, 'rb') as f:
        G = pickle.load(f)

    M = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            ks = set()
            for k in range(n):
                if G.has_edge(i, k) and G.has_edge(k, j):
                    ks.add(k)
            if len(ks) == 1:
                M[i][j] = ks.pop()
            else:
                print(f"Ambiguity in determining M[{i}][{j}]. Possible values: {ks}")
                M[i][j] = None  # Or handle accordingly

    return M

def main():
    # Specify the table index and size
    table_index = 1  # Change as needed
    n = 4  # Size of the multiplication table

    # Construct the graph filename
    #graph_filename = f'graph_{table_index}.pkl'
    graph_filename = f'graph_1_4x4.pkl'
    # Reconstruct the multiplication table
    M = reconstruct_multiplication_table_from_graph(graph_filename, n)

    # Print the reconstructed multiplication table
    print("Reconstructed multiplication table M:")
    for row in M:
        print(row)

if __name__ == '__main__':
    main()
