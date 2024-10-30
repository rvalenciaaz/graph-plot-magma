import ast
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from tqdm import tqdm
from scipy.signal import convolve2d

# Step 1: Read matrices from a file
def read_matrices(file_path):
    matrices = []
    with open(file_path, 'r') as file:
        for line in file:
            matrix_list = ast.literal_eval(line.strip())
            matrix_array = np.array(matrix_list)
            matrices.append(matrix_array)
    return matrices

# Step 2: Sort each matrix in descending order by row and column sums
def sort_matrix_descending(matrix):
    row_sums = matrix.sum(axis=1)
    sorted_row_indices = np.argsort(row_sums)
    matrix_sorted_rows = matrix[sorted_row_indices, :]

    column_sums = matrix_sorted_rows.sum(axis=0)
    sorted_col_indices = np.argsort(column_sums)
    sorted_matrix = matrix_sorted_rows[:, sorted_col_indices]
    
    return sorted_matrix

# Updated Finite Difference Transform Function for First Derivative
def finite_difference_transform(matrix):
    # Define the coefficients for the 4th-order centered finite difference approximation of the first derivative
    fd_coefficients = [1, -4, 0, 4, -1]  # Positions: [-2, -1, 0, 1, 2]

    # Convert coefficients to a NumPy array
    fd_coefficients = np.array(fd_coefficients)

    # Create convolution kernels for x and y directions
    kernel_x = fd_coefficients.reshape(1, -1)  # Shape: (1, 5)
    kernel_y = fd_coefficients.reshape(-1, 1)  # Shape: (5, 1)

    # Apply convolution in the x-direction (first derivative)
    transformed_x = convolve2d(
        matrix,
        kernel_x,
        mode='same',
        boundary='fill',
        fillvalue=0
    )

    # Apply convolution in the y-direction (first derivative)
    transformed_y = convolve2d(
        matrix,
        kernel_y,
        mode='same',
        boundary='fill',
        fillvalue=0
    )

    # Compute the gradient magnitude
    transformed_matrix = np.sqrt(transformed_x**2 + transformed_y**2)

    return transformed_matrix

# Laplacian Transform Function
def laplacian_transform(matrix):
    laplacian_kernel = np.array([[0, 1, 0],
                                 [1, -4, 1],
                                 [0, 1, 0]])

    transformed_matrix = convolve2d(
        matrix,
        laplacian_kernel,
        mode='same',
        boundary='fill',
        fillvalue=0
    )
    return transformed_matrix

# Transform Matrix Function
def transform_matrix(matrix, method='finite_difference'):
    if method == 'finite_difference':
        transformed_matrix = finite_difference_transform(matrix)
    elif method == 'laplacian':
        transformed_matrix = laplacian_transform(matrix)
    else:
        raise ValueError(f"Unknown transformation method: {method}")
    return transformed_matrix

# Step 4: Plot and save each matrix as a separate file (optional)
def plot_and_save_matrices(matrices, output_dir='matrix_plots', annotate=True):
    os.makedirs(output_dir, exist_ok=True)
    all_values = np.concatenate([matrix.flatten() for matrix in matrices])
    min_val, max_val = all_values.min(), all_values.max()
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(vmin=min_val, vmax=max_val)

    for i, matrix in enumerate(tqdm(matrices, desc="Plotting matrices")):
        fig, ax = plt.subplots(figsize=(4, 4))
        im = ax.imshow(matrix, cmap=cmap, norm=norm)
        
        if annotate:
            for y in range(matrix.shape[0]):
                for x in range(matrix.shape[1]):
                    ax.text(x, y, f"{matrix[y, x]:.2f}", ha='center', va='center', color="white", fontsize=8, weight='bold')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Matrix {i + 1}', fontsize=10, weight='bold')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        plt.savefig(f"{output_dir}/matrix_{i + 1}.png")
        plt.close(fig)

# Step 5: Main function to execute all steps
def main(input_file, output_file, method):
    matrices = read_matrices(input_file)
    transformed_matrices = []
    for matrix in tqdm(matrices, desc="Processing matrices"):
        sorted_matrix = sort_matrix_descending(matrix)
        transformed_matrix = transform_matrix(sorted_matrix, method=method)
        transformed_matrices.append(transformed_matrix)

    # Write transformed matrices to the output file
    with open(output_file, 'w') as file:
        for matrix in tqdm(transformed_matrices, desc="Writing matrices to output file"):
            file.write(f"{matrix.tolist()}\n")

    # Optional: Plot and save matrices
    # plot_and_save_matrices(transformed_matrices)

# Set up argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and transform matrices from a file.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing matrices.")
    parser.add_argument("output_file", type=str, help="Path to the output file to save transformed matrices.")
    parser.add_argument("-m", "--method", type=str, choices=['finite_difference', 'laplacian'], default='finite_difference',
                        help="Transformation method: 'finite_difference' or 'laplacian'.")
    parser.add_argument("-y", "--yes", action="store_true", help="Automatically overwrite output file if it exists.")
    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        exit(1)

    # Check if the output file exists
    if os.path.isfile(args.output_file):
        if args.yes:
            os.remove(args.output_file)
        else:
            print(f"Error: Output file '{args.output_file}' already exists. Use -y to overwrite.")
            exit(1)

    # Run the script with the specified input and output files and transformation method
    main(args.input_file, args.output_file, args.method)