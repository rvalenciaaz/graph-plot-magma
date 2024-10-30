import numpy as np

def transform_matrix(matrix):
    rows, cols = matrix.shape
    transformed_matrix = np.zeros((rows, cols), dtype=int)
    
    for i in range(rows):
        for j in range(cols):
            a_ij = matrix[i, j]
            a_i1j = matrix[i-1, j] if i-1 >= 0 else 0
            a_ij1 = matrix[i, j-1] if j-1 >= 0 else 0
            a_i1j1 = matrix[i-1, j-1] if (i-1 >= 0 and j-1 >= 0) else 0
            transformed_matrix[i, j] = a_ij - a_i1j - a_ij1 + a_i1j1
            
    return transformed_matrix

def read_matrices(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
    matrices = [eval(line.strip()) for line in content]
    return [np.array(matrix) for matrix in matrices]

def write_matrices(filename, matrices):
    with open(filename, 'w') as file:
        for matrix in matrices:
            file.write(f"{matrix.tolist()}\n")

def main(input_file, output_file):
    matrices = read_matrices(input_file)
    transformed_matrices = [transform_matrix(matrix) for matrix in matrices]
    write_matrices(output_file, transformed_matrices)

# Run the main function with input and output file paths
input_file = 'transformed_matrices.txt'
output_file = 'transformed_matrices_2_iter.txt'
main(input_file, output_file)
