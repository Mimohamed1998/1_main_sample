import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports from src
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.logger import get_logger
from src.utils.config import load_yaml_config

# Initialize the logger for this script
logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting configuration test pipeline...")

    try:
        logger.debug("Attempting to load 'paths.yaml'")
        paths = load_yaml_config('paths.yaml')
        logger.info(f"Loaded paths successfully: {paths}")

        logger.debug("Attempting to load 'variables.yaml'")
        variables = load_yaml_config('variables.yaml')
        logger.info("Loaded variables successfully.")

    except FileNotFoundError as e:
        logger.error(f"A required configuration file is missing: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during execution: {e}", exc_info=True)
    
    # Just to demonstrate a warning clearly:
    logger.warning("This script is for testing purposes only. Do not use in production.")
    
    # Demonstrate an error log without actually crashing the script
    logger.error("This is a simulated error message to demonstrate error logging.")
    
    logger.info("Pipeline test completed.")
