import yaml
from pathlib import Path

def get_project_root() -> Path:
    """Returns the project root directory."""
    # This script is at: src/utils/config.py
    # So the project root is 2 parents up.
    return Path(__file__).resolve().parent.parent.parent

def load_yaml_config(yaml_filename: str) -> dict:
    """Loads a YAML configuration file from the conf directory."""
    project_root = get_project_root()
    config_path = project_root / 'conf' / yaml_filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
