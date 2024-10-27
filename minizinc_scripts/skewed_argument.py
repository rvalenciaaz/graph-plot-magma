import numpy as np
import argparse

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
            matrices.append(np.array(matrix)*2)
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
            result_matrix[i, j] = 0.5 * (-matrix[i, j]+ matrix[i, j-1]- matrix[i-1, j-1]+matrix[i-1, j])
    
    return result_matrix

def insert_row_and_column(matrix):
    """
    Insert a new row and column at the front of the matrix.
    Both the new row and the new column will contain values from 0 to len(matrix),
    and they will share the 0 at the top-left corner.
    """
    num_rows = matrix.shape[0]
    
    # Create a range from 0 to len(matrix)
    new_values = np.arange(num_rows + 1)*2  # [0, 1, 2, ..., len(matrix)]
    
    # Insert the new column at the front (axis=1 for columns)
    matrix_with_column = np.insert(matrix, 0, new_values[1:], axis=1)  # Insert column excluding the first 0
    
    # Insert the new row at the front (axis=0 for rows)
    matrix_with_row_and_column = np.insert(matrix_with_column, 0, new_values, axis=0)
    
    return matrix_with_row_and_column

def save_matrices_to_txt(file_path, matrices):
    """
    Save a list of matrices to a txt file. Each matrix will be saved in a new line.
    """
    with open(file_path, 'w') as f:
        for matrix in matrices:
            # Convert the numpy matrix to a string and write to the file
            f.write(str(matrix.tolist()) + '\n')

def main():
    # Set up argument parser to accept input and output file paths as arguments
    parser = argparse.ArgumentParser(description="Process and save modified matrices from a text file.")
    parser.add_argument('input_file', type=str, help="Path to the file containing the matrices")
    parser.add_argument('output_file', type=str, help="Path to the output file where modified matrices will be saved")

    # Parse the arguments
    args = parser.parse_args()

    # Load matrices from the file
    matrices = load_matrix_from_txt(args.input_file)

    # List to store the modified matrices
    modified_matrices = []

    # Process each matrix loaded from the file
    for idx, matrix in enumerate(matrices):
        print(f"\nOriginal Matrix {idx + 1}:")
        print(matrix)
        
        # Insert row and column with values [0, 1, 2, ..., len(matrix)] into the original matrix
        matrix_with_inserted_row_col = insert_row_and_column(matrix)
        print(f"\nMatrix {idx + 1} with inserted row and column:")
        print(matrix_with_inserted_row_col)
        
        # Modify the matrix with the custom formula after insertion
        modified_matrix = calculate_modified_matrix(matrix_with_inserted_row_col)
        modified_matrix = modified_matrix[1:, 1:]  # Remove the first row and column from the result
        
        print(f"\nModified Matrix {idx + 1}:")
        print(modified_matrix)

        # Check if the modified matrix is symmetrical
        is_symmetric = np.array_equal(modified_matrix, modified_matrix.T)
        print(f"Is Modified Matrix {idx + 1} Symmetrical? {'Yes' if is_symmetric else 'No'}")

        # Calculate and print the sum of the diagonal
        diagonal_sum = np.trace(modified_matrix)
        print(f"Sum of Diagonal for Modified Matrix {idx + 1}: {diagonal_sum}")
        
        # Compute and print the determinant of the modified matrix
        if modified_matrix.size > 0:  # Ensure the matrix is not empty
            determinant = np.linalg.det(modified_matrix)
            print(f"Determinant of Modified Matrix {idx + 1}: {determinant}")
        else:
            determinant = None
            print("The modified matrix is empty; determinant cannot be calculated.")
        
        # Compute and print row and column sums
        row_sums = np.sum(modified_matrix, axis=1)
        col_sums = np.sum(modified_matrix, axis=0)
        print(f"Sum of Rows for Modified Matrix {idx + 1}: {np.sum(row_sums)}")
        print(f"Sum of Columns for Modified Matrix {idx + 1}: {np.sum(col_sums)}")
        
        modified_matrices.append(modified_matrix)

    # Save the modified matrices to the output file
    save_matrices_to_txt(args.output_file, modified_matrices)
    print(f"\nModified matrices have been saved to {args.output_file}")

if __name__ == "__main__":
    main()
