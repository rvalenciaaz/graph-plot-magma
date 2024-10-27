import sympy as sp  # For symbolic math operations and solving equations
import itertools  # To generate binary matrices
import argparse  # For command-line argument parsing
import ast  # To safely evaluate strings as Python literals, used for reading matrices from files

# Set matrix size
n = 4  # Adjust the size as needed
specified_index = 51329  # Set the index of the binary matrix to test (0-based index)

# Function to generate the specific binary matrix at a given index
def get_binary_matrix_at_index(n, index):
    values = list(itertools.product([0, 1], repeat=n*n))[index]
    return [list(values[i * n:(i + 1) * n]) for i in range(n)]

# Function to read multiple matrices from a text file
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

# Function to check if matrix is valid
def is_valid_matrix(matrix):
    return all(element in [-1, 0, 1] for element in matrix)

# Compute a_star from a (Forward process) with given coefficients
def forward_a_star(a_values, n, coeff_matrix):
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)
    equations = []
    
    for i in range(n):
        for j in range(n):
            sum_expr = 0
            for i_prime in range(i + 1):
                for j_prime in range(j + 1):
                    sum_expr += coeff_matrix[i_prime][j_prime] * a[i_prime, j_prime]
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1) - sum_expr)
            equations.append(equation)
    
    a_subs = {a[i, j]: a_values[i][j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a_star[i, j] for i in range(n) for j in range(n)])
    a_star_values = {k: v.subs(a_subs) for k, v in solution.items()}
    
    a_star_matrix = sp.Matrix(n, n, lambda i, j: a_star_values[a_star[i, j]])
    return a_star_matrix

# Main function to process only one binary matrix
def main():
    parser = argparse.ArgumentParser(description="Compute a_star from a (forward) using a specific binary coefficient matrix.")
    parser.add_argument("n", type=int, help="The size of the matrix (n x n)")
    parser.add_argument("input_filename", type=str, help="The path to the file containing the input matrix values")
    parser.add_argument("output_filename", type=str, help="The path for the output file to save results")
    
    args = parser.parse_args()
    global n  
    n = args.n
    input_filename = args.input_filename
    output_filename = args.output_filename
    
    # Read matrices from file
    matrices = read_matrices_from_file(input_filename)
    results = []
    
    # Retrieve the specific binary coefficient matrix
    coeff_matrix = get_binary_matrix_at_index(n, specified_index)
    
    # Process each input matrix
    for matrix_values in matrices:
        result_matrix = forward_a_star(matrix_values, n, coeff_matrix)
        if is_valid_matrix(result_matrix):
            print(f"\nCoefficient matrix {specified_index + 1} passed:")
            sp.pprint(sp.Matrix(coeff_matrix))
            results.append(result_matrix)
        else:
            print(f"\nCoefficient matrix {specified_index + 1} did not pass.")
    
    # Write all results to the output file
    write_matrices_to_file(results, output_filename)

if __name__ == "__main__":
    main()