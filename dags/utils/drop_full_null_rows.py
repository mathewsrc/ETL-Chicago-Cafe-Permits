import polars as pl
from loguru import logger

@logger.catch
def drop_full_null_rows(df: pl.DataFrame):
    """
    Drop rows from a polars DataFrame if all values in a row are null.

    Args:
        df (pl.DataFrame): The input polars DataFrame from which rows with all-null values will be removed.

    Returns:
        pl.DataFrame: A new polars DataFrame with rows removed if all values in the row are null.

    Example:
        >>> df = pl.DataFrame({
        ...     "A": [None, None, 3],
        ...     "B": [2, None, None],
        ...     "C": [4, None, 6]
        ... })
        >>> cleaned_df = drop_full_rows_nulls(df)
        >>> print(cleaned_df)
           A    B  C
        0  None 2  4
        2  3  None  6

    Note:
        - This function removes rows where all values in the row are null.
        - If you want to remove rows with any null value, consider using `df.drop_nulls()` instead.
    """
    return df.filter(~pl.all_horizontal(pl.all().is_null()))
