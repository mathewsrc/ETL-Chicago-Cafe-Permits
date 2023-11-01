import polars as pl
from dags.utils.rename_columns import rename_columns_name

def test_rename_columns_name():
    # Create a test DataFrame with original column names
    df = pl.DataFrame({'PERMIT NUMBER': [1, 2], 'ACCOUNT NUMBER': [3, 4]})

    # Call the function to rename columns
    df = rename_columns_name(df)

    # Check if the columns have been renamed correctly
    expected_columns = ['permit_number', 'account_number']
    assert df.columns == expected_columns

    # Create another test DataFrame with original column names
    df = pl.DataFrame({'PERMIT NUMBER': [1, 2], 'ACCOUNT NUMBER': [3, 4], 'SITE NUMBER': [5, 6]})

    # Call the function to rename columns
    df = rename_columns_name(df)

    # Check if the columns have been renamed correctly
    expected_columns = ['permit_number', 'account_number', 'site_number']
    assert df.columns == expected_columns

    # Create another test DataFrame with original column names
    df = pl.DataFrame({'PERMIT NUMBER': [1, 2], 'ACCOUNT NUMBER': [3, 4], 'SITE NUMBER': [5, 6], 'LEGAL NAME': ['a', 'b']})

    # Call the function to rename columns
    df = rename_columns_name(df)

    # Check if the columns have been renamed correctly
    expected_columns = ['permit_number', 'account_number', 'site_number', 'legal_name']
    assert df.columns == expected_columns