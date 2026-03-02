import pandas as pd
import re

class DataCleaner:
    """Tools for simple data cleaning."""
    
    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans column names:
        - Removes leading/trailing whitespace
        - Converts to snake_case
        - Removes special characters (except underscores)
        """
        new_columns = []
        for col in df.columns:
            # Strip and lowercase
            clean_name = col.strip().lower()
            # Replace spaces and hyphens with underscores
            clean_name = re.sub(r'[\s\-#]+', '_', clean_name)
            # Remove any non-alphanumeric or non-underscore characters
            clean_name = re.sub(r'[^\w]', '', clean_name)
            # Remove multiple underscores
            clean_name = re.sub(r'_+', '_', clean_name)
            # Remove trailing underscore
            clean_name = clean_name.strip('_')
            new_columns.append(clean_name)
            
        df.columns = new_columns
        return df
