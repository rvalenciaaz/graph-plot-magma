import re
import pandas as pd

def extract_tables_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match the operation tables and adjacency matrices
    operation_pattern = re.compile(r"Operation Table:\s*(\[\[.*?\]\])", re.DOTALL)
    adjacency_pattern = re.compile(r"Adjacency Matrix:\s*(\[\[.*?\]\])", re.DOTALL)

    # Extract all operation tables and adjacency matrices
    operation_tables = operation_pattern.findall(content)
    adjacency_matrices = adjacency_pattern.findall(content)

    # Convert the string representations into actual lists
    operation_tables = [table for table in operation_tables]
    adjacency_matrices = [matrix for matrix in adjacency_matrices]

    # Create a DataFrame with the parsed data
    df = pd.DataFrame({
        "Operation Table": operation_tables,
        "Adjacency Matrix": adjacency_matrices
    })

    return df

# Replace 'path_to_your_file.txt' with the path to your input file
file_path = 'adjacency_4x4_original.txt'
df = extract_tables_from_file(file_path)

# Display the generated table
df=df.sort_values(["Operation Table","Adjacency Matrix"])

# Optionally save the table to a CSV file
df.to_csv('output_table.csv', index=False)