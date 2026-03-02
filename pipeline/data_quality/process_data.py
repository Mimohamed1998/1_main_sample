import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path to allow absolute imports from src
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.logger import get_logger
from src.tools.cleaner import DataCleaner

logger = get_logger(__name__)

def main():
    logger.info("Starting Processed Data Pipeline...")
    
    # 1. Define paths based on project root
    staged_path = project_root / 'data' / 'staged' / 'staged_users.csv'
    processed_path = project_root / 'data' / 'processed' / 'processed_users.csv'
    
    # Ensure processed directory exists
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 2. Load the staged dataset
        logger.debug(f"Loading staged data from {staged_path}")
        df = pd.read_csv(staged_path)
        
        # 3. Apply Data Quality Strategies
        logger.debug("Applying Data Quality Null Strategies...")
        df_processed = DataCleaner.apply_dq_strategies(df)
        
        # 4. Save to the processed directory
        logger.debug(f"Saving processed dataset to {processed_path}")
        df_processed.to_csv(processed_path, index=False)
        
        logger.info(f"Dataset successfully processed and saved.")
        logger.info(f"Original shape: {df.shape} | New shape: {df_processed.shape}")
        
    except FileNotFoundError as e:
        logger.error(f"Missing required file or directory: {e}")
    except Exception as e:
        logger.error(f"Pipeline failed unexpectedly: {e}", exc_info=True)

if __name__ == "__main__":
    main()
