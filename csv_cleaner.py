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

def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', fill_value: Optional[dict] = None) -> pd.DataFrame:
    """
    Handle missing values in the dataframe using different strategies.

    Parameters:
    - df: DataFrame to handle missing values
    - strategy: The strategy to use for handling missing values.
                Options: 'drop', 'fill', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill'
    - fill_value: A dictionary with column names as keys and the fill values as values, for custom filling.
    
    Returns:
    - df: DataFrame with handled missing values
    """
    if strategy == 'drop':
        # Drop rows with any missing values
        df = df.dropna()
        logger.info("Dropped rows with missing values.")
    
    elif strategy == 'fill':
        # Fill missing values with a specific value for each column (if fill_value is provided)
        if fill_value is not None:
            df = df.fillna(fill_value)
            logger.info(f"Filled missing values with the provided values: {fill_value}")
        else:
            logger.warning("No fill value provided for 'fill' strategy.")
    
    elif strategy == 'mean':
        # Fill missing values with the mean of the column
        df = df.fillna(df.mean())
        logger.info("Filled missing values with column means.")
    
    elif strategy == 'median':
        # Fill missing values with the median of the column
        df = df.fillna(df.median())
        logger.info("Filled missing values with column medians.")
    
    elif strategy == 'mode':
        # Fill missing values with the mode (most frequent value) of the column
        df = df.fillna(df.mode().iloc[0])
        logger.info("Filled missing values with column mode.")
    
    elif strategy == 'forward_fill':
        # Forward fill missing values (use previous row value)
        df = df.ffill()
        logger.info("Forward-filled missing values.")
    
    elif strategy == 'backward_fill':
        # Backward fill missing values (use next row value)
        df = df.bfill()
        logger.info("Backward-filled missing values.")
    
    else:
        logger.error(f"Unknown strategy '{strategy}' for handling missing values.")
        raise ValueError(f"Unknown strategy '{strategy}' for handling missing values.")
    
    return df

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

        # Handle missing values (Example: 'drop', 'fill', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill')
        df = handle_missing_values(df, strategy='mean')  # Example: Use 'mean' to fill missing values
        logger.info("Handled missing values")

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
