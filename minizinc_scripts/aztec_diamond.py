import networkx as nx
import numpy as np

def aztec_diamond_graph(n):
    """
    Constructs the directed graph for the Aztec Diamond of order n.
    
    Parameters:
    - n: Order of the Aztec Diamond
    
    Returns:
    - G: A directed NetworkX graph representing the Aztec Diamond
    - sources: List of source nodes
    - sinks: List of sink nodes
    """
    G = nx.DiGraph()
    
    # Aztec Diamond coordinates range from (-n, -n) to (n, n) with |x| + |y| <= n
    for x in range(-n, n + 1):
        for y in range(-n, n + 1):
            if abs(x) + abs(y) <= n:
                G.add_node((x, y))
    
    # Define possible moves: right (1, 0), up-right (1, 1), down-right (1, -1)
    moves = [(1, 0), (1, 1), (1, -1)]
    
    # Create edges according to valid moves and boundary conditions
    for node in G.nodes:
        for move in moves:
            neighbor = (node[0] + move[0], node[1] + move[1])
            if neighbor in G:
                G.add_edge(node, neighbor)
    
    # Sources: nodes on the left edge where x = -n
    sources = [node for node in G.nodes if node[0] == -n]
    
    # Sinks: nodes on the right edge where x = n
    sinks = [node for node in G.nodes if node[0] == n]
    
    return G, sources, sinks

def count_paths(G, sources, sinks):
    """
    Counts the number of paths from each source to each sink.
    
    Parameters:
    - G: Directed graph
    - sources: List of source nodes
    - sinks: List of sink nodes
    
    Returns:
    - P: Path matrix as a NumPy array where P[i][j] is the number of paths from sources[i] to sinks[j]
    """
    # Topologically sort the graph
    try:
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        raise ValueError("The graph contains a cycle, which is not allowed for counting paths.")
    
    # Initialize the path matrix
    P = np.zeros((len(sources), len(sinks)), dtype=int)
    
    # Count paths from each source to each sink
    for i, source in enumerate(sources):
        # Reset path counts for each source
        path_counts = {node: 0 for node in G.nodes}
        path_counts[source] = 1  # One path to the source itself
        
        # Traverse in topological order
        for node in topo_order:
            for neighbor in G.successors(node):
                path_counts[neighbor] += path_counts[node]
        
        # Populate the path matrix for current source
        for j, sink in enumerate(sinks):
            P[i][j] = path_counts[sink]
    
    return P

def main(n):
    G, sources, sinks = aztec_diamond_graph(n)
    P = count_paths(G, sources, sinks)
    print(f"Path Matrix P_{n}:")
    print(P)

if __name__ == "__main__":
    # Example usage for n=2
    main(2)

