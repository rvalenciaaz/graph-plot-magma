#!/bin/bash

# Loop from 1 to 24
for i in {1..24}
do
    # Dynamically set the input and output matrix filenames
    input_matrix_file="order_8_matrix_${i}_transformed.txt"
    output_matrix_file="order_8_matrix_${i}_zeros.txt"
    
    echo "Running iteration $i with input file $input_matrix_file and output file $output_matrix_file..."
    
    # Run the Python script with the dynamically named input and output matrix files
    #python every_operation_fdiff_laplace.py "$input_matrix_file" "$output_matrix_file" -o 2 -y
    #python every_operation_fdiff.py "$input_matrix_file" "$output_matrix_file" -y
    python check_zeros.py "$input_matrix_file" "$output_matrix_file"
done

echo "All iterations completed."
