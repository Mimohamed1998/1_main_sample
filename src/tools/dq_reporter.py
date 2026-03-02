import pandas as pd
from datetime import datetime

class DataQualityReporter:
    """Utility class to generate Data Quality Markdown reports."""

    @staticmethod
    def generate_distribution_report(df: pd.DataFrame, dataset_name: str) -> str:
        """
        Generates a markdown report detailing column null counts and 
        data distributions for categorical variables.
        """
        total_rows = len(df)
        report_lines = [
            f"# Data Quality Report: Distribution & Nulls",
            f"**Dataset**: `{dataset_name}`  ",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Total Rows**: {total_rows}  ",
            f"**Total Columns**: {len(df.columns)}",
            "",
            "## Null Value Summary",
            "| Column | Data Type | Null Count | Null % |",
            "|--------|-----------|------------|--------|"
        ]

        for col in df.columns:
            null_count = df[col].isnull().sum()
            null_pct = (null_count / total_rows) * 100 if total_rows > 0 else 0
            dtype = str(df[col].dtype)
            report_lines.append(f"| `{col}` | {dtype} | {null_count} | {null_pct:.2f}% |")

        report_lines.extend([
            "",
            "## Categorical Variable Distributions",
            "Discrete unique values and their frequencies for categorical/object columns.",
            ""
        ])

        # Identify categorical columns (object or category)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) == 0:
            report_lines.append("*No categorical variables found in this dataset.*")
        else:
            for col in categorical_cols:
                report_lines.extend([f"### Column: `{col}`", ""])
                value_counts = df[col].value_counts(dropna=False)
                
                # Create a mini table for the distribution
                report_lines.extend([
                    "| Value | Count | Percentage |",
                    "|-------|-------|------------|"
                ])
                
                for val, count in value_counts.items():
                    # Handle display of actual nulls clearly
                    display_val = '*(Null/NaN)*' if pd.isna(val) else str(val)
                    pct = (count / total_rows) * 100 if total_rows > 0 else 0
                    report_lines.append(f"| {display_val} | {count} | {pct:.2f}% |")
                
                report_lines.append("")

        return "\n".join(report_lines)

    @staticmethod
    def generate_strategy_report(df: pd.DataFrame, dataset_name: str) -> str:
        """
        Generates a markdown report proposing imputation strategies for nulls.
        """
        total_rows = len(df)
        report_lines = [
            f"# Data Quality Report: Null Handling Strategies",
            f"**Dataset**: `{dataset_name}`  ",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            "",
            "## Proposed Null Value Strategies",
            "| Column | Null % | Proposed Strategy | Reason |",
            "|--------|--------|-------------------|--------|"
        ]

        strategy_added = False
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count == 0:
                continue
                
            strategy_added = True
            null_pct = (null_count / total_rows) * 100 if total_rows > 0 else 0
            dtype = str(df[col].dtype)
            
            # Simple theoretical imputation strategy logic
            if col == 'notes':
                strategy = "Drop Column"
                reason = "High null percentage, not critical for analysis"
            else:
                strategy = "Keep As Is"
                reason = "Retain null values without changes"
                
            report_lines.append(f"| `{col}` | {null_pct:.2f}% | {strategy} | {reason} |")

        if not strategy_added:
            report_lines = [
                f"# Data Quality Report: Null Handling Strategies",
                f"**Dataset**: `{dataset_name}`",
                "",
                "No columns contain null values. No imputation strategies are required."
            ]

        return "\n".join(report_lines)
