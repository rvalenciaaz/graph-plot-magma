#!/bin/bash

# Check if a file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Input file provided as an argument
input_file="$1"

# Create the output file name by replacing "output" with "cleaned" in the input file name
output_file="${input_file/output/cleaned}"

# Remove lines containing '---------' or '==========' and save to the new file
grep -v -e '----------' -e '==========' "$input_file" > "$output_file"

# Print completion message
echo "Cleaned file saved as $output_file"
