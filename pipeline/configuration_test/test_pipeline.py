import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports from src
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.config import load_yaml_config

if __name__ == "__main__":
    try:
        print("Loading configurations...v2")
        paths = load_yaml_config('paths.yaml')
        variables = load_yaml_config('variables.yaml')

        print("\n--- Paths ---")
        print("All paths:", paths)
        print("Raw data path:", paths.get('raw_data'))
        print("Models path:", paths.get('model_dir'))

        print("\n--- Variables ---")
        print("Model Name:", variables.get('model_name'))
        if 'hyperparameters' in variables:
            print("Learning Rate:", variables['hyperparameters'].get('learning_rate'))
            print("Max Depth:", variables['hyperparameters'].get('max_depth'))
            
        print("\nConfigurations loaded successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
