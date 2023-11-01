import polars as pl
from loguru import logger

@logger.catch
def rename_columns_name(df):
    """
    Rename columns to lowercase in a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input Polars DataFrame.

    Returns:
        pl.DataFrame: The Polars DataFrame with column names in lowercase.

    Example:
        >>> df = pl.DataFrame({
        ...     "Column1": [1, 2, 3],
        ...     "Column2": ["A", "B", "C"]
        ... })
        >>> df = lower_column(df)
        >>> print(df)
        shape: (3, 2)
        ┌────────┬────────┐
        │ column1│ column2│
        │ int    │ str    │
        ╞════════╪════════╡
        │ 1      │ "A"    │
        ├────────┼────────┤
        │ 2      │ "B"    │
        ├────────┼────────┤
        │ 3      │ "C"    │
        └────────┴────────┘

    Note:
        This function renames columns in the input Polars DataFrame to lowercase.
        It creates a new DataFrame with column names converted to lowercase while keeping the original data intact.

    """
    return df.select([pl.col(col).alias(col.lower().replace(" ", "_")) for col in df.columns])