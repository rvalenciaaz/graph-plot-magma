import numpy as np

def load_matrix_from_txt(file_path):
    """
    Load matrices from a txt file where each matrix is defined on a single row 
    in the format [[0, 1, 2, 3], [4, 5, 6, 7], ...]
    """
    matrices = []
    with open(file_path, 'r') as f:
        for line in f:
            # Evaluate each line as a Python list
            matrix = eval(line.strip())
            matrices.append(np.array(matrix))
    return matrices

def calculate_modified_matrix(matrix):
    """
    Calculate 1/2(a_{i-1,j}+a_{i,j-1}-a_{i-1,j-1}-a_{i,j}) for the given matrix.
    """
    # Initialize a result matrix
    result_matrix = np.zeros_like(matrix, dtype=float)
    
    # Iterate starting from the second row and second column
    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            # Apply the given formula
            result_matrix[i, j] = 0.5 * (matrix[i-1, j] + matrix[i, j-1] - matrix[i-1, j-1] - matrix[i, j])
    
    return result_matrix

def main():
    # Specify the file path
    file_path = 'order_8_magmas.txt'  # Replace with the path to your matrices.txt file

    # Load matrices from the file
    matrices = load_matrix_from_txt(file_path)

    # Calculate modified matrices for each matrix loaded from the file
    for idx, matrix in enumerate(matrices):
        print(f"\nOriginal Matrix {idx + 1}:")
        print(matrix)
        modified_matrix = calculate_modified_matrix(matrix)
        modified_matrix=modified_matrix[1:,1:]
        print(f"\nModified Matrix {idx + 1}:")
        print(modified_matrix)

if __name__ == "__main__":
    main()