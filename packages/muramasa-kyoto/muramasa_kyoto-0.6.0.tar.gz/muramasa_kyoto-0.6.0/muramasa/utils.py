import pandas as pd

def load_data(file_path):
    """
    Load data from a CSV file.
    
    Args:
    file_path (str): Path to the CSV file
    
    Returns:
    pd.DataFrame: Loaded data
    """
    return pd.read_csv(file_path)

def preprocess_data(df):
    """
    Preprocess the data by removing unnecessary columns.
    
    Args:
    df (pd.DataFrame): Input data
    
    Returns:
    pd.DataFrame: Preprocessed data
    """
    columns_to_drop = ['plasmid_id']
    if 'sequence' in df.columns:
        columns_to_drop.append('sequence')
    return df.drop(columns_to_drop, axis=1, errors='ignore')