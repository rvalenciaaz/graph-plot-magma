import ast
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Find matrices with maximum zeros from an input file and save them to an output file.")
parser.add_argument('input_file', type=str, help="Path to the input file containing matrices.")
parser.add_argument('output_file', type=str, help="Path to the output file where results will be saved.")
args = parser.parse_args()

# Load the data from the input file
with open(args.input_file, 'r') as file:
    lines = file.readlines()

# Initialize variables to track the maximum zero count and corresponding matrices and indices
max_zeros = 0
matrices_with_max_zeros = []
row_indices_with_max_zeros = []

# Process each row, which represents a matrix
for row_index, line in enumerate(lines, start=1):  # Start enumeration from 1
    matrix = ast.literal_eval(line.strip())  # Parse the line as a list of lists (matrix)
    
    # Count zeros in the matrix
    zero_count = sum(row.count(0) for row in matrix)
    
    # Update if this matrix has more zeros than the previous maximum
    if zero_count > max_zeros:
        max_zeros = zero_count
        matrices_with_max_zeros = [matrix]
        row_indices_with_max_zeros = [row_index]
    elif zero_count == max_zeros:
        matrices_with_max_zeros.append(matrix)
        row_indices_with_max_zeros.append(row_index)

# Save results to the output file
with open(args.output_file, 'w') as output_file:
    for idx, matrix in zip(row_indices_with_max_zeros, matrices_with_max_zeros):
        output_file.write(f"Matrix at row index {idx} with {max_zeros} zeros:\n")
        output_file.write(str(matrix) + "\n")
        output_file.write("="*40 + "\n")

print(f"Results saved to {args.output_file}")