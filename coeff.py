import sympy as sp
import argparse
import ast  # To safely evaluate the matrix format from text

# Set default size and coefficient matrix globally
n = 4
coeff_matrix = sp.Matrix([[1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]])

# Function to read multiple matrices from a text file
def read_matrices_from_file(filename):
    matrices = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                matrix = sp.Matrix(ast.literal_eval(line))  # Convert each line to a SymPy matrix
                matrices.append(matrix)
    return matrices

# Function to write results to an output file
def write_matrices_to_file(matrices, filename):
    with open(filename, 'w') as file:
        for matrix in matrices:
            file.write(str(matrix.tolist()).replace(" ", "") + "\n")
    print(f"\nResults have been saved to {filename}")

# Function to print row and column sums, and check for symmetry
def analyze_matrix(matrix):
    row_sums = [sum(matrix.row(i)) for i in range(matrix.shape[0])]
    col_sums = [sum(matrix.col(i)) for i in range(matrix.shape[1])]
    is_symmetric = matrix.equals(matrix.T)

    print("Row sums:", row_sums)
    print("Column sums:", col_sums)
    print("Symmetric:", is_symmetric)

# Compute a_star from a (Forward process) with constant coefficients
def forward_a_star(a_values, n):
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)
    equations = []
    
    for i in range(n):
        for j in range(n):
            sum_expr = sum(coeff_matrix[i_prime, j_prime] * a[i_prime, j_prime] 
                           for i_prime in range(i + 1) for j_prime in range(j + 1))
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1) - sum_expr)
            equations.append(equation)
    
    # Substitute values into a and solve for a_star
    a_subs = {a[i, j]: a_values[i, j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a_star[i, j] for i in range(n) for j in range(n)])
    a_star_values = {k: v.subs(a_subs) for k, v in solution.items()}
    
    a_star_matrix = sp.Matrix(n, n, lambda i, j: a_star_values[a_star[i, j]])
    print("\nComputed matrix `a_star` from forward process with constant coefficients:")
    sp.pprint(a_star_matrix)
    analyze_matrix(a_star_matrix)
    return a_star_matrix

# Compute a from a_star (Inverse process) with constant coefficients
def inverse_a_star(a_star_values, n):
    a = sp.MatrixSymbol('a', n, n)
    a_star = sp.MatrixSymbol('a_star', n, n)
    equations = []
    
    for i in range(n):
        for j in range(n):
            sum_expr = sum(coeff_matrix[i_prime, j_prime] * a[i_prime, j_prime] 
                           for i_prime in range(i + 1) for j_prime in range(j + 1))
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1) - sum_expr)
            equations.append(equation)
    
    # Substitute values into a_star and solve for a
    a_star_subs = {a_star[i, j]: a_star_values[i, j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a[i, j] for i in range(n) for j in range(n)])
    print(solution)
    a_reconstructed_values = {k: v.subs(a_star_subs) for k, v in solution.items()}
    
    a_reconstructed_matrix = sp.Matrix(n, n, lambda i, j: a_reconstructed_values[a[i, j]])
    print("\nReconstructed matrix `a` from inverse process with constant coefficients:")
    sp.pprint(a_reconstructed_matrix)
    analyze_matrix(a_reconstructed_matrix)
    return a_reconstructed_matrix

# Main function to handle arguments and run the specified computation on each matrix
def main():
    parser = argparse.ArgumentParser(description="Compute a_star from a (forward) or a from a_star (inverse) for multiple matrices with constant coefficients.")
    parser.add_argument("n", type=int, help="The size of the matrix (n x n)")
    parser.add_argument("input_filename", type=str, help="The path to the file containing the input matrix values")
    parser.add_argument("output_filename", type=str, help="The path for the output file to save results")
    parser.add_argument("process", choices=['forward', 'inverse'], help="Specify 'forward' for a -> a_star or 'inverse' for a_star -> a")
    
    args = parser.parse_args()
    global n, coeff_matrix  # Update global values
    n = args.n
    coeff_matrix = sp.Matrix([[1,1,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,1]])

    input_filename = args.input_filename
    output_filename = args.output_filename
    process = args.process
    
    # Read all matrices from the file
    matrices = read_matrices_from_file(input_filename)
    results = []

    # Process each matrix according to the specified process
    for matrix_values in matrices:
        if process == 'forward':
            result = forward_a_star(matrix_values, n)
        elif process == 'inverse':
            result = inverse_a_star(matrix_values, n)
        results.append(result)

    # Write all results to the output file
    write_matrices_to_file(results, output_filename)

if __name__ == "__main__":
    main()
