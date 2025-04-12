import pandas as pd
import numpy as np
import sys
import logging
from datetime import datetime
import re
from typing import List, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def detect_outliers(df: pd.DataFrame, columns: List[str], n_std: float = 3) -> pd.DataFrame:
    """Remove outliers based on z-score method."""
    for column in columns:
        if df[column].dtype in ['int64', 'float64']:
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df = df[z_scores < n_std]
    return df

def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Advanced string cleaning for text columns."""
    for col in df.select_dtypes(include='object').columns:
        # Convert to string type first to handle any mixed types
        df[col] = df[col].astype(str)
        
        # Apply cleaning operations
        df[col] = df[col].apply(lambda x: x.strip()  # Remove leading/trailing whitespace
                               .lower()  # Convert to lowercase
                               .replace('\n', ' ')  # Remove newlines
                               .replace('\t', ' ')  # Remove tabs
                               )
        
        # Remove multiple spaces
        df[col] = df[col].apply(lambda x: re.sub(' +', ' ', x))
        
        # Remove special characters but keep basic punctuation
        df[col] = df[col].apply(lambda x: re.sub(r'[^a-z0-9\s.,!?-]', '', x))
    
    return df

def infer_and_convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Infer and convert column types."""
    # Try to convert numeric columns
    for col in df.columns:
        # Skip date columns
        if 'date' in col.lower():
            continue
            
        # Try converting to numeric
        try:
            num_values = pd.to_numeric(df[col], errors='coerce')
            # If more than 80% of values are numeric, convert the column
            if num_values.notna().sum() / len(df) > 0.8:
                df[col] = num_values
        except:
            continue
    
    return df

def convert_dates(df: pd.DataFrame, date_formats: Optional[List[str]] = None) -> pd.DataFrame:
    """Convert date columns with multiple format support."""
    if date_formats is None:
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', 
                       '%d-%m-%Y', '%m-%d-%Y', '%Y%m%d']
    
    for col in df.columns:
        if 'date' in col.lower():
            # Try each format
            for date_format in date_formats:
                try:
                    df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
                    if df[col].notna().sum() > 0:  # If successful conversion
                        break
                except:
                    continue
    
    return df

def generate_data_profile(df: pd.DataFrame) -> None:
    """Generate basic data profile."""
    logger.info("\nData Profile:")
    logger.info(f"Total Rows: {len(df)}")
    logger.info(f"Total Columns: {len(df.columns)}")
    logger.info("\nMissing Values:")
    logger.info(df.isnull().sum())
    logger.info("\nData Types:")
    logger.info(df.dtypes)
    logger.info("\nSample Values:")
    logger.info(df.head())

def main():
    try:
        # Get input and output file names from command line
        if len(sys.argv) != 3:
            logger.error("Usage: python csv_cleaner.py input_file.csv output_file.csv")
            sys.exit(1)
            
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        # Read CSV
        logger.info(f"Reading file: {input_file}")
        df = pd.read_csv(input_file, low_memory=False)
        
        # Generate initial profile
        logger.info("Initial data profile:")
        generate_data_profile(df)

        # Cleaning steps
        logger.info("Starting data cleaning process...")
        
        # Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(df)} duplicate rows")

        # Clean string columns
        df = clean_string_columns(df)
        logger.info("Completed string cleaning")

        # Convert dates
        df = convert_dates(df)
        logger.info("Completed date conversion")

        # Infer and convert types
        df = infer_and_convert_types(df)
        logger.info("Completed type inference and conversion")

        # Remove outliers from numeric columns
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) > 0:
            initial_rows = len(df)
            df = detect_outliers(df, numeric_columns)
            logger.info(f"Removed {initial_rows - len(df)} rows with outliers")

        # Remove rows with null values
        initial_rows = len(df)
        df = df.dropna()
        logger.info(f"Removed {initial_rows - len(df)} rows with null values")

        # Generate final profile
        logger.info("\nFinal data profile:")
        generate_data_profile(df)

        # Save clean file
        df.to_csv(output_file, index=False)
        logger.info(f"✅ Success! Cleaned file saved as: {output_file}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
