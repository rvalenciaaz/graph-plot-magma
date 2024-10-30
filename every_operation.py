import ast
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse

# Step 1: Read matrices from a file
def read_matrices(file_path):
    with open(file_path, 'r') as file:
        matrices = [ast.literal_eval(line.strip()) for line in file]
    return matrices

# Step 2: Sort each matrix in descending order by row and column sums
def sort_matrix_descending(matrix):
    matrix_sorted_rows = sorted(matrix, key=sum)
    transposed_matrix = list(map(list, zip(*matrix_sorted_rows)))
    transposed_matrix_sorted = sorted(transposed_matrix, key=sum)
    sorted_matrix = list(map(list, zip(*transposed_matrix_sorted)))
    print(sorted_matrix)
    return sorted_matrix

# Step 3: Transform the matrix with cumulative sum logic
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

# Step 4: Plot matrices
def plot_matrices(matrices, matrices_per_row=4):
    num_matrices = len(matrices)
    num_rows = (num_matrices + matrices_per_row - 1) // matrices_per_row
    cmap = mcolors.ListedColormap(["#f7f7f7", "#add8e6", "#87ceeb", "#4682b4", "#4169e1"])
    bounds = [-2, -1, 0, 1, 2, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    plt.figure(figsize=(matrices_per_row * 3.5, num_rows * 3.5))
    for i, matrix in enumerate(matrices):
        ax = plt.subplot(num_rows, matrices_per_row, i + 1)
        im = ax.imshow(matrix, cmap=cmap, norm=norm)
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                ax.text(x, y, f"{matrix[y][x]}", ha='center', va='center', color="black", fontsize=8, weight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f'Matrix {i + 1}', fontsize=10, weight='bold')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.show()

# Step 5: Main function to execute all steps
def main(input_file):
    matrices = read_matrices(input_file)
    sorted_matrices = [sort_matrix_descending(matrix) for matrix in matrices]
    transformed_matrices = [transform_matrix(np.array(matrix)) for matrix in sorted_matrices]
    plot_matrices(transformed_matrices)

# Set up argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and plot matrices from a file.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing matrices.")
    args = parser.parse_args()

    # Run the script with the specified input file
    main(args.input_file)