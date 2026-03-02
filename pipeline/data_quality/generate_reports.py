import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path to allow absolute imports from src
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.logger import get_logger
from src.tools.cleaner import DataCleaner
from src.tools.dq_reporter import DataQualityReporter

logger = get_logger(__name__)

def main():
    logger.info("Starting Data Quality Reporting Pipeline...")
    
    # 1. Define paths based on project root
    raw_path = project_root / 'data' / 'raw' / 'raw_users.csv'
    staged_path = project_root / 'data' / 'staged' / 'staged_users.csv'
    dist_report_path = project_root / 'data' / 'dq_report' / 'distribution_reports' / 'staged_users_distribution.md'
    strategy_report_path = project_root / 'data' / 'dq_report' / 'strategy_reports' / 'staged_users_strategy.md'
    
    try:
        # 2. Load the raw dataset
        logger.debug(f"Loading raw data from {raw_path}")
        df = pd.read_csv(raw_path)
        
        # 3. Clean the column names using DataCleaner
        logger.debug("Cleaning column names...")
        df = DataCleaner.clean_column_names(df)
        
        # 4. Save to the staged directory
        logger.debug(f"Saving cleaned dataset to {staged_path}")
        df.to_csv(staged_path, index=False)
        logger.info(f"Dataset securely staged.")
        
        # 5. Generate Data Quality Reports
        logger.info("Generating Data Quality Reports...")
        dataset_name = "staged_users"
        
        # Distribution Report
        dist_report_content = DataQualityReporter.generate_distribution_report(df, dataset_name)
        with open(dist_report_path, 'w') as f:
            f.write(dist_report_content)
        logger.debug(f"Distribution report saved to {dist_report_path}")
            
        # Strategy Report
        strategy_report_content = DataQualityReporter.generate_strategy_report(df, dataset_name)
        with open(strategy_report_path, 'w') as f:
            f.write(strategy_report_content)
        logger.debug(f"Strategy report saved to {strategy_report_path}")
            
        logger.info("Data Quality Reporting Pipeline completed successfully!")
        
    except FileNotFoundError as e:
        logger.error(f"Missing required file or directory: {e}")
    except Exception as e:
        logger.error(f"Pipeline failed unexpectedly: {e}", exc_info=True)

if __name__ == "__main__":
    main()
