import pickle
import networkx as nx

def load_graph(file_path):
    """Load a pickled graph from a file."""
    with open(file_path, 'rb') as file:
        graph = pickle.load(file)
    return graph

def analyze_graph(graph):
    """Perform analysis on the graph and return key properties."""
    analysis = {}
    analysis['Number of Nodes'] = graph.number_of_nodes()
    analysis['Number of Edges'] = graph.number_of_edges()
    analysis['Is Directed'] = nx.is_directed(graph)
    analysis['Degree Sequence'] = [d for _, d in graph.degree()]
    analysis['In Degrees'] = dict(graph.in_degree())
    analysis['Out Degrees'] = dict(graph.out_degree())

    return analysis

def analyze_graph_files(file_list):
    """Analyze multiple graph files and print the results."""
    for file_path in file_list:
        print(f"\nAnalyzing graph from file: {file_path}")
        try:
            graph = load_graph(file_path)
            analysis = analyze_graph(graph)
            # Print the analysis results
            for key, value in analysis.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

# Example usage: list of files to analyze
file_list = ['graph_1_8x8.pkl','graph_2_8x8.pkl','graph_6_8x8.pkl','graph_512_8x8.pkl','graph_513_8x8.pkl', 'graph_516_8x8.pkl', 'graph_518_8x8.pkl', 'graph_1536_8x8.pkl']

# Analyze all graphs in the file list
analyze_graph_files(file_list)
