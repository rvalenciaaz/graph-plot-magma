import ast

def read_matrices_from_file(file_path):
    with open(file_path, 'r') as file:
        matrices = [ast.literal_eval(line.strip()) for line in file]
    return matrices

def sort_matrix_descending(matrix):
    # Sort rows by row sum in descending order
    matrix_sorted_rows = sorted(matrix, key=sum) #reverse=True)
    
    # Transpose to sort columns by column sum in descending order
    transposed_matrix = list(map(list, zip(*matrix_sorted_rows)))
    transposed_matrix_sorted = sorted(transposed_matrix, key=sum) #reverse=True)
    
    # Transpose back to get sorted columns in the original layout
    sorted_matrix = list(map(list, zip(*transposed_matrix_sorted)))
    return sorted_matrix

def main(input_file, output_file):
    matrices = read_matrices_from_file(input_file)
    sorted_matrices = [sort_matrix_descending(matrix) for matrix in matrices]
    
    with open(output_file, 'w') as file:
        for matrix in sorted_matrices:
            file.write(f"{matrix}\n")

# Specify the input and output file paths
input_file = 'order_8_magmas.txt'
output_file = 'sorted_matrices_descending_8.txt'

# Run the sorting and output
main(input_file, output_file)