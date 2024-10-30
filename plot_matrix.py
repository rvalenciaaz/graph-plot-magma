import ast
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Function to load matrices from a file
def load_matrices(file_path):
    with open(file_path, 'r') as file:
        matrices = [ast.literal_eval(line.strip()) for line in file if line.strip()]
    return matrices

# Function to create a grid plot for the matrices
def plot_matrices(matrices, matrices_per_row=4):
    num_matrices = len(matrices)
    num_rows = (num_matrices + matrices_per_row - 1) // matrices_per_row  # Calculate rows needed

    # Define a discrete color map with lighter colors
    cmap = mcolors.ListedColormap(["#f7f7f7", "#add8e6", "#87ceeb", "#4682b4", "#4169e1"])
    bounds = [-2, -1, 0, 1, 2, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Adjust figure size
    plt.figure(figsize=(matrices_per_row * 3.5, num_rows * 3.5))
    
    # Loop through each matrix and plot it
    for i, matrix in enumerate(matrices):
        ax = plt.subplot(num_rows, matrices_per_row, i + 1)
        im = ax.imshow(matrix, cmap=cmap, norm=norm)
        
        # Show the value in each cell
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                value = matrix[y][x]
                ax.text(x, y, f"{value}", ha='center', va='center', color="black", fontsize=8, weight='bold')

        # Remove axis ticks for a cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add title to each subplot
        ax.set_title(f'Matrix {i + 1}', fontsize=10, weight='bold')
        
        # Add a color bar for each matrix
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Tight layout for spacing between plots
    plt.tight_layout()
    plt.show()

# Load matrices from file and plot them
file_path = 'transformed_matrices.txt'  # Replace with your actual file path
matrices = load_matrices(file_path)
plot_matrices(matrices)
