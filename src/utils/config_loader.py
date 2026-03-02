import json
import os
from jsonschema import validate, ValidationError

def load_loot_config(file_path):
    """
    Loads and validates a loot configuration from a JSON file.
    
    Args:
        file_path (str): Path to the JSON configuration file.
        
    Returns:
        dict: The validated configuration data.
    """
    # Try relative to the script's root if the path doesn't exist directly.
    if not os.path.exists(file_path):
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(root_dir, file_path)
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Loot config file not found: {file_path}")
        
    with open(file_path, 'r') as f:
        config = json.load(f)
        
    # Optional validation against the schema if it exists.
    schema_path = os.path.join(os.path.dirname(file_path), "loot_schema.json")
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as s:
            schema = json.load(s)
            try:
                validate(instance=config, schema=schema)
            except ValidationError as e:
                print(f"Loot config validation failed: {e.message}")
                # We can choose to either raise or just warn.
                
    return config

def load_retention_config(file_path):
    """
    Loads a retention configuration from a JSON file.
    """
    if not os.path.exists(file_path):
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(root_dir, file_path)
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Retention config file not found: {file_path}")
        
    with open(file_path, 'r') as f:
        config = json.load(f)
        
    return config
