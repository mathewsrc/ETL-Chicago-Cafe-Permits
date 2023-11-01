import polars as pl

def drop_missing(df: pl.DataFrame):
    """
    Drops rows containing null values in specified columns.

    Args:
        df (pl.DataFrame): The DataFrame to process.

    Returns:
        pl.DataFrame: A new DataFrame with rows removed where there are null values in the following columns:
            - permit_number
            - city
            - legal_name
            - doing_business_as_name

    Example:
        df = pl.DataFrame({
            "permit_number": [1, 2, None, 4, 5],
            "city": ["New York", "Los Angeles", "Chicago", None, "Miami"],
            "legal_name": ["ABC Inc.", "XYZ Corp.", None, "LMN Ltd.", "PQR Co."],
            "doing_business_as_name": ["ABC", "XYZ", "DEF", None, "PQR"]
        })
        cleaned_df = drop_missing(df)

    Note:
        This function will remove rows that have null values in any of the specified columns.

    """
    return df.drop_nulls(subset=["permit_number", "city", "legal_name", "doing_business_as_name"])
