import ast
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse
import os
from tqdm import tqdm

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

# Step 3: Transform the matrix with cumulative sum logic
def transform_matrix(matrix):
    padded_matrix = np.pad(matrix, ((1, 0), (1, 0)), mode='constant', constant_values=0)
    transformed_matrix = matrix - padded_matrix[0:-1, 1:] - padded_matrix[1:, 0:-1] + padded_matrix[0:-1, 0:-1]
    return transformed_matrix

# Step 4: Plot and save each matrix as a separate file
def plot_and_save_matrices(matrices, output_dir='matrix_plots', annotate=True):
    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine color map bounds based on the range of data
    all_values = np.concatenate([matrix.flatten() for matrix in matrices])
    min_val, max_val = all_values.min(), all_values.max()
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(vmin=min_val, vmax=max_val)

    # Plot and save each matrix
    for i, matrix in enumerate(tqdm(matrices, desc="Plotting matrices")):
        fig, ax = plt.subplots(figsize=(4, 4))
        im = ax.imshow(matrix, cmap=cmap, norm=norm)
        
        if annotate:
            for y in range(matrix.shape[0]):
                for x in range(matrix.shape[1]):
                    ax.text(x, y, f"{matrix[y, x]}", ha='center', va='center', color="white", fontsize=8, weight='bold')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Matrix {i + 1}', fontsize=10, weight='bold')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # Save the plot as a separate file
        plt.savefig(f"{output_dir}/matrix_{i + 1}.png")
        plt.close(fig)  # Close the figure to save memory

# Step 5: Main function to execute all steps
def main(input_file, output_file):
    matrices = read_matrices(input_file)
    
    sorted_matrices = []
    transformed_matrices = []
    for matrix in tqdm(matrices, desc="Processing matrices"):
        sorted_matrix = sort_matrix_descending(matrix)
        transformed_matrix = transform_matrix(sorted_matrix)
        sorted_matrices.append(sorted_matrix)
        transformed_matrices.append(transformed_matrix)

    # Write transformed matrices to the output file
    with open(output_file, 'w') as file:
        for matrix in tqdm(transformed_matrices, desc="Writing matrices to output file"):
            file.write(f"{matrix.tolist()}\n")

    #plot_and_save_matrices(transformed_matrices)

# Set up argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and plot matrices from a file.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing matrices.")
    parser.add_argument("output_file", type=str, help="Path to the output file to save transformed matrices.")
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

    # Run the script with the specified input and output files
    main(args.input_file, args.output_file)