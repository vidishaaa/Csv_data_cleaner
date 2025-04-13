#!/bin/bash

echo "Running CSV Cleaner Script 🧽"

INPUT=$1
OUTPUT=$2

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: ./clean.sh input.csv output.csv"
  exit 1
fi

python3 clean_csv.py "$INPUT" "$OUTPUT"
echo "Cleaning complete! Output saved to $OUTPUT 🎉"
