---
description: How to perform agentic data cleaning on a dataset
---
// turbo-all
1. **Analyze Data Structure**: Use `head` or `pandas` to read the first few rows of the dataset. Identify messy column names, mixed data types, and missing values.
2. **Standardize Columns**: Use the `DataCleaner` tool to normalize column names to `snake_case`.
3. **Data Quality Audit**: Run the `QualityAuditor` to generate a report on nulls and outliers.
4. **Identify Anomalies**: Manually (agentically) inspect columns with high null rates or inconsistent formats (e.g., dates, phone numbers).
5. **Apply Cleaning Strategies**: 
    - Fix casing (e.g., convert "ACTIVE", "Active", "active" to a single standard).
    - Impute or handle missing values based on column context.
    - Format dates and numbers.
6. **Verify and Export**: Run a final check on the cleaned data and save it to the silver/gold layer.
7. **Generate Summary**: Provide the user with a list of specific transformations made.
