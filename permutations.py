import itertools
import ast
import os
from tqdm import tqdm

def invert_permutation(p):
    """
    Returns the inverse of a given permutation p.
    """
    n = len(p)
    p_inv = [0] * n
    for i in range(n):
        p_inv[p[i]] = i
    return p_inv

def generate_alternative_matrices(m, output_filename):
    """
    Generates all alternative operation tables by applying all permutations
    to the elements of the original operation table m, and writes them to the output file.

    Parameters:
    - m: Original operation table (list of lists or tuples).
    - output_filename: The name of the output file to write the alternative matrices.
    """
    n = len(m)
    total_permutations = factorial(n)

    with open(output_filename, 'w') as f_output:
        # Generate all permutations of the elements
        for p in tqdm(itertools.permutations(range(n)), total=total_permutations, desc="Generating permutations"):
            p_inv = invert_permutation(p)
            m_p = []

            # Build the permuted table
            for x in range(n):
                row = []
                for y in range(n):
                    # Apply the permutation to inputs and outputs
                    x_pre = p_inv[x]
                    y_pre = p_inv[y]
                    new_value = p[m[x_pre][y_pre]]
                    row.append(new_value)
                m_p.append(row)
            # Write the permuted matrix to the output file
            f_output.write(str(m_p) + '\n')

def read_matrices_from_file(filename):
    """
    Reads multiple matrices from a file, each row as a separate matrix.

    Parameters:
    - filename: The name of the file containing the matrices, one per line.

    Returns:
    - A list of matrices, where each matrix is a list of lists.
    """
    matrices = []
    with open(filename, 'r') as f:
        for line in f:
            matrix = ast.literal_eval(line.strip())
            matrices.append(matrix)
    return matrices

def factorial(n):
    """
    Computes the factorial of n.

    Parameters:
    - n: An integer

    Returns:
    - n!
    """
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

# Main execution block
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate alternative operation tables by permuting elements for multiple matrices.')
    parser.add_argument('input_filename', help='Input file containing the operation tables, one per line.')
    parser.add_argument('output_prefix', help='Prefix for output files to write the alternative matrices.')
    args = parser.parse_args()

    # Read all matrices from the input file
    matrices = read_matrices_from_file(args.input_filename)

    # Process each matrix individually
    for idx, matrix in enumerate(matrices):
        # Define a unique output filename based on the prefix and matrix index
        output_filename = f"{args.output_prefix}_matrix_{idx + 1}.txt"

        # Generate all alternative matrices and write them to the output file
        generate_alternative_matrices(matrix, output_filename)

        print(f"Alternative matrices for matrix {idx + 1} have been generated and saved to '{output_filename}'.")