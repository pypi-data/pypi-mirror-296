import pandas as pd
import os

def load_sample_data(file_path, save_to_dbfs="/dbfs/tmp/sample_data.csv"):
    """
    Load CSV file from the given file path, save it to DBFS, and return the DataFrame.
    
    Parameters:
    - file_path: Path to the CSV file (local or DBFS).
    - save_to_dbfs: Optional path to save the DataFrame on DBFS for sharing between notebooks.
    
    Returns:
    - DataFrame (if loaded successfully).
    """
    try:
        df = pd.read_csv(file_path)
        # Save the DataFrame to DBFS for retrieval from another notebook
        df.to_csv(save_to_dbfs, index=False)
        print(f"DataFrame saved to {save_to_dbfs}")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
