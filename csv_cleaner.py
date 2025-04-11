import pandas as pd
import sys

# Get input and output file names from command line
input_file = sys.argv[1]
output_file = sys.argv[2]

# Read CSV
df = pd.read_csv(input_file)

# Cleaning steps
df = df.dropna()  # Remove nulls
df = df.drop_duplicates()  # Remove duplicate rows

# Trim strings and make lowercase
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip().str.lower()

# Convert date columns
for col in df.columns:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Save clean file
df.to_csv(output_file, index=False)

print("✅ Done! Cleaned file saved as:", output_file)
