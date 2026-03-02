import pandas as pd
import numpy as np
import json
import os

def ingest_community_data(file_path):
    """
    Ingests observed community pull data from CSV or JSON.
    Expected format: 
    - CSV: column 'trials_to_success'
    - JSON: list of integers
    """
    _, ext = os.path.splitext(file_path)
    
    try:
        if ext.lower() == '.csv':
            df = pd.read_csv(file_path)
            if 'trials_to_success' in df.columns:
                return df['trials_to_success'].values
            else:
                raise ValueError("CSV must contain 'trials_to_success' column.")
        
        elif ext.lower() == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return np.array(data)
                else:
                    raise ValueError("JSON must be a list of integers.")
        
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
            
    except Exception as e:
        return {"error": str(e)}

def calculate_distribution_counts(data, bins=None):
    """
    Converts raw trial data into frequency counts for Chi-Squared testing.
    """
    if bins is None:
        # Default bins: 1-10, 11-20, ..., 91-100, 100+
        bins = list(range(0, 101, 10)) + [float('inf')]
        
    counts, _ = np.histogram(data, bins=bins)
    return counts, bins
