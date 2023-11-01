import polars as pl

def drop_full_null_columns(df: pl.DataFrame):
    """
    Drops columns from a DataFrame where all values are null.

    Args:
        df (pl.DataFrame): The DataFrame from which to drop columns.

    Returns:
        pl.DataFrame: The DataFrame with columns dropped where all values are null.

    Example:
        >>> df = pl.DataFrame({
        ...     "A": [1, None, 3],
        ...     "B": [None, None, None],
        ...     "C": [4, 5, 6]
        ... })
        >>> cleaned_df = drop_full_null_columns(df)
        >>> print(cleaned_df)
           A  C
        0  1  4
        2  3  6

    Note:
        - This function removes columns where all values in the column are null.
        - If you want to remove columns with any null value, consider using a different approach.
    """
    return df[[s.name for s in df if not (s.null_count() == df.height)]]
