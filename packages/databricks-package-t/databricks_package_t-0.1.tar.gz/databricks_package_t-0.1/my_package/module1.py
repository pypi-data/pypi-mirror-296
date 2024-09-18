# my_package/module1.py
import pandas as pd

def load_sample_data(file_path):
    """
    Load CSV file from the given file path and return a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
    
 
