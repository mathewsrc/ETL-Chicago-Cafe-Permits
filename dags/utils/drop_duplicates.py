from loguru import logger
import polars as pl

@logger.catch
def drop_duplicates(df: pl.DataFrame):
    """
    Remove duplicate rows from a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input Polars DataFrame.

    Returns:
        pl.DataFrame: The Polars DataFrame with duplicate rows removed.

    Example:
        >>> df = pl.DataFrame({
        ...     "Column1": [1, 2, 2, 3, 4],
        ...     "Column2": ["A", "B", "B", "C", "D"]
        ... })
        >>> df = drop_duplicates(df)
        >>> print(df)
        shape: (4, 2)
        ┌────────┬────────┐
        │ column1│ column2│
        │ int    │ str    │
        ╞════════╪════════╡
        │ 1      │ "A"    │
        ├────────┼────────┤
        │ 2      │ "B"    │
        ├────────┼────────┤
        │ 3      │ "C"    │
        ├────────┼────────┤
        │ 4      │ "D"    │
        └────────┴────────┘

    Note:
        This function removes duplicate rows from the input Polars DataFrame.
        It creates a new DataFrame with duplicate rows removed, but it does not modify the original DataFrame.

    """
    return df.unique(keep="first")