import sympy as sp
import argparse
import ast  # To safely evaluate the matrix format from text

# Function to read multiple matrices from the text file
def read_matrices_from_file(filename):
    matrices = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                matrix = ast.literal_eval(line)  # Evaluate each line as a list
                matrices.append(matrix)
    return matrices

# Function to write results to an output file
def write_matrices_to_file(matrices, filename):
    with open(filename, 'w') as file:
        for matrix in matrices:
            file.write(str(matrix.tolist()).replace(" ", "") + "\n")
    print(f"\nResults have been saved to {filename}")

# Function to print row and column sums, and check for symmetry
def analyze_matrix(matrix, index):
    print(f"\nProcessing matrix: {index}")
    row_sums = [sum(row) for row in matrix.tolist()]
    col_sums = [sum(matrix[:, i]) for i in range(matrix.shape[1])]
    is_symmetric = matrix == matrix.T

    # Check if row and column sums are identical up to permutation
    row_col_identical = sorted(row_sums) == sorted(col_sums)
    
    # Compute the sum of the sums of rows and columns
    sum_of_row_sums = sum(row_sums)
    sum_of_col_sums = sum(col_sums)

    # Extract unique elements, sort them, and display
    unique_elements = sorted(set(matrix))

    print("Row sums:", row_sums)
    print("Column sums:", col_sums)
    print("Symmetric:", is_symmetric)
    print("Row and column sums identical (up to permutation):", row_col_identical)
    print("Sum of row sums:", sum_of_row_sums)
    print("Sum of column sums:", sum_of_col_sums)
    print("Unique elements (sorted):", unique_elements)

# Compute a_star from a (Forward process)
def forward_a_star(a_values, n, index):
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)
    equations = []
    for i in range(n):
        for j in range(n):
            i_prime, j_prime = sp.symbols('i_prime j_prime')
            sum_expr = sp.summation(a[i_prime, j_prime], (i_prime, 0, i), (j_prime, 0, j))
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1) -1 - sum_expr)
            equations.append(equation)
    
    # Substitute values into a and solve for a_star
    a_subs = {a[i, j]: a_values[i][j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a_star[i, j] for i in range(n) for j in range(n)])
    a_star_values = {k: v.subs(a_subs) for k, v in solution.items()}
    
    # Create the computed a_star matrix
    a_star_matrix = sp.Matrix(n, n, lambda i, j: a_star_values[a_star[i, j]])
    print(f"\nComputed matrix `a_star` from forward process (matrix {index}):")
    sp.pprint(a_star_matrix)
    analyze_matrix(a_star_matrix, index)
    return a_star_matrix

# Compute a from a_star (Inverse process)
def inverse_a_star(a_star_values, n, index):
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)
    equations = []
    for i in range(n):
        for j in range(n):
            i_prime, j_prime = sp.symbols('i_prime j_prime')
            sum_expr = sp.summation(a[i_prime, j_prime], (i_prime, 0, i), (j_prime, 0, j))
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1)-1  - sum_expr)
            equations.append(equation)
    
    # Substitute values into a_star and solve for a
    a_star_subs = {a_star[i, j]: a_star_values[i][j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a[i, j] for i in range(n) for j in range(n)])
    a_reconstructed_values = {k: v.subs(a_star_subs) for k, v in solution.items()}
    
    # Create the reconstructed a matrix
    a_reconstructed_matrix = sp.Matrix(n, n, lambda i, j: a_reconstructed_values[a[i, j]])
    print(f"\nReconstructed matrix `a` from inverse process (matrix {index}):")
    sp.pprint(a_reconstructed_matrix)
    analyze_matrix(a_reconstructed_matrix, index)
    return a_reconstructed_matrix

# Main function to handle arguments and run the specified computation on each matrix
def main():
    parser = argparse.ArgumentParser(description="Compute a_star from a (forward) or a from a_star (inverse) for multiple matrices.")
    parser.add_argument("n", type=int, help="The size of the matrix (n x n)")
    parser.add_argument("input_filename", type=str, help="The path to the file containing the input matrix values")
    parser.add_argument("output_filename", type=str, help="The path for the output file to save the initial results")
    parser.add_argument("process", choices=['forward', 'inverse'], help="Specify 'forward' for a -> a_star or 'inverse' for a_star -> a")
    
    args = parser.parse_args()
    n = args.n
    input_filename = args.input_filename
    output_filename = args.output_filename
    process = args.process
    
    # Read all matrices from the file
    matrices = read_matrices_from_file(input_filename)
    initial_results = []

    # Process each matrix according to the specified process
    for index, matrix_values in enumerate(matrices, start=1):
        if process == 'forward':
            result = forward_a_star(matrix_values, n, index)
        elif process == 'inverse':
            result = inverse_a_star(matrix_values, n, index)
        initial_results.append(result)

    # Write initial results to the output file
    write_matrices_to_file(initial_results, output_filename)

if __name__ == "__main__":
    main()