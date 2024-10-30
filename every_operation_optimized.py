import ast
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse

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
    sorted_row_indices = np.argsort(row_sums)  # Descending order
    matrix_sorted_rows = matrix[sorted_row_indices, :]

    column_sums = matrix_sorted_rows.sum(axis=0)
    sorted_col_indices = np.argsort(column_sums)  # Descending order
    sorted_matrix = matrix_sorted_rows[:, sorted_col_indices]
    
    return sorted_matrix

# Step 3: Transform the matrix with cumulative sum logic
def transform_matrix(matrix):
    padded_matrix = np.pad(matrix, ((1, 0), (1, 0)), mode='constant', constant_values=0)
    transformed_matrix = matrix - padded_matrix[0:-1, 1:] - padded_matrix[1:, 0:-1] + padded_matrix[0:-1, 0:-1]
    return transformed_matrix

# Step 4: Plot matrices
def plot_matrices(matrices, matrices_per_row=4, annotate=True):
    num_matrices = len(matrices)
    num_rows = (num_matrices + matrices_per_row - 1) // matrices_per_row

    # Determine color map bounds based on the range of data
    all_values = np.concatenate([matrix.flatten() for matrix in matrices])
    min_val, max_val = all_values.min(), all_values.max()
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(vmin=min_val, vmax=max_val)

    fig, axes = plt.subplots(num_rows, matrices_per_row, figsize=(matrices_per_row * 3.5, num_rows * 3.5))
    
    # Ensure axes is a flat array
    axes = np.array(axes).flatten()

    for i, (ax, matrix) in enumerate(zip(axes, matrices)):
        im = ax.imshow(matrix, cmap=cmap, norm=norm)
        if annotate:
            for y in range(matrix.shape[0]):
                for x in range(matrix.shape[1]):
                    ax.text(x, y, f"{matrix[y, x]}", ha='center', va='center', color="white", fontsize=8, weight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Matrix {i + 1}', fontsize=10, weight='bold')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    # Hide any unused axes
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    plt.show()

# Step 5: Main function to execute all steps
def main(input_file, output_file):
    matrices = read_matrices(input_file)
    sorted_matrices = [sort_matrix_descending(matrix) for matrix in matrices]
    transformed_matrices = [transform_matrix(matrix) for matrix in sorted_matrices]

    # Write transformed matrices to the output file
    with open(output_file, 'w') as file:
        for matrix in transformed_matrices:
            file.write(f"{matrix.tolist()}\n")

    plot_matrices(transformed_matrices)

# Set up argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and plot matrices from a file.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing matrices.")
    parser.add_argument("output_file", type=str, help="Path to the output file to save transformed matrices.")
    args = parser.parse_args()

    # Run the script with the specified input and output files
    main(args.input_file, args.output_file)