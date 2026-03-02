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
                # Provide a more helpful error message including the file being validated
                raise ValueError(f"Loot config schema validation failed in {os.path.basename(file_path)}: {e.message}")
                
    # Forensic Sanity Checks
    base_prob = config.get("base_prob", 0.0)
    if base_prob < 0 or base_prob > 1.0:
        raise ValueError(f"Nonsensical Architecture: base_prob must be between 0 and 1. Found: {base_prob}")
        
    cost = config.get("cost_per_pull_usd", 0.0)
    if cost < 0:
        raise ValueError(f"Nonsensical Architecture: cost_per_pull_usd cannot be negative. Found: {cost}")
        
    if "expected_meta_lifespan_days" in config and config["expected_meta_lifespan_days"] <= 0:
        raise ValueError(f"Nonsensical Architecture: expected_meta_lifespan_days must be > 0. Found: {config['expected_meta_lifespan_days']}")
        
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
