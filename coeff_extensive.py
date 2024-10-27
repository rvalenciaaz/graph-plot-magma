from tqdm import tqdm  # Import tqdm for progress tracking
import sympy as sp
import itertools
import argparse
import ast  # To safely evaluate the matrix format from text

# Set matrix size
n = 4  # Adjust the size as needed

# Function to generate all binary matrices of size n x n
def generate_binary_matrices(n):
    binary_matrices = []
    for values in itertools.product([0, 1], repeat=n*n):
        matrix = [list(values[i * n:(i + 1) * n]) for i in range(n)]
        binary_matrices.append(matrix)
    return binary_matrices

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
                    # Use the specific coefficient matrix for this iteration
                    sum_expr += coeff_matrix[i_prime][j_prime] * a[i_prime, j_prime]
            equation = sp.Eq(a_star[i, j], (i + 1) + (j + 1) - sum_expr)
            equations.append(equation)
    
    # Substitute values into a and solve for a_star
    a_subs = {a[i, j]: a_values[i][j] for i in range(n) for j in range(n)}
    solution = sp.solve(equations, [a_star[i, j] for i in range(n) for j in range(n)])
    a_star_values = {k: v.subs(a_subs) for k, v in solution.items()}
    
    # Create the computed a_star matrix
    a_star_matrix = sp.Matrix(n, n, lambda i, j: a_star_values[a_star[i, j]])
    return a_star_matrix

# Check if the matrix contains only elements -1, 0, or 1
def is_valid_matrix(matrix):
    return all(element in [-1, 0, 1] for element in matrix)

# Main function to handle arguments and run the specified computation on each matrix
def main():
    parser = argparse.ArgumentParser(description="Compute a_star from a (forward) or a from a_star (inverse) for multiple matrices with binary coefficient matrix exploration.")
    parser.add_argument("n", type=int, help="The size of the matrix (n x n)")
    parser.add_argument("input_filename", type=str, help="The path to the file containing the input matrix values")
    parser.add_argument("output_filename", type=str, help="The path for the output file to save results")
    
    args = parser.parse_args()
    global n  # Update the global `n` if it's passed as an argument
    n = args.n

    input_filename = args.input_filename
    output_filename = args.output_filename
    
    # Read all matrices from the file
    matrices = read_matrices_from_file(input_filename)
    results = []
    
    # Generate all possible binary coefficient matrices
    binary_matrices = generate_binary_matrices(n)

    # Process each input matrix and find a valid coefficient matrix
    for matrix_values in matrices:
        found_valid = False
        print(f"\nTesting input matrix: {matrix_values}")
        
        # Use tqdm to track progress for binary_matrices
        for index, coeff_matrix in enumerate(tqdm(binary_matrices, desc="Testing coefficient matrices")):
            result_matrix = forward_a_star(matrix_values, n, coeff_matrix)
            if is_valid_matrix(result_matrix):
                print(f"Coefficient matrix {index + 1} passed:")
                sp.pprint(sp.Matrix(coeff_matrix))
                results.append(result_matrix)
                found_valid = True
                break

        if not found_valid:
            print("No valid coefficient matrix found for this input matrix.")

    # Write all results to the output file
    write_matrices_to_file(results, output_filename)

if __name__ == "__main__":
    main()