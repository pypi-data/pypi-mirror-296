import pandas as pd

def load_data_from_dbfs(dbfs_path="/dbfs/tmp/sample_data.csv"):
    """
    Load the DataFrame from the saved DBFS path.
    
    Parameters:
    - dbfs_path: Path where the CSV file is saved on DBFS.
    
    Returns:
    - DataFrame if the file exists, None if not.
    """
    try:
        df = pd.read_csv(dbfs_path)
        print(f"Data loaded from {dbfs_path}")
        return df
    except Exception as e:
        print(f"Error loading data from DBFS: {e}")
        return None

def display_data(df):
    """
    Display the DataFrame.
    """
    if df is not None:
        print("DataFrame:")
        print(df.head())
    else:
        print("No data to display.")
