import polars as pl
from dags.utils.rename_columns import rename_columns_name  # Replace 'your_module' with the actual module name

def test_rename_columns_name():
    # Create a test DataFrame with mixed case column names
    test_data = {
        "Column1": [1, 2, 3],
        "Column2": ["A", "B", "C"]
    }
    df = pl.DataFrame(test_data)

    # Call the function to rename columns to lowercase
    result_df = rename_columns_name(df)

    # Define the expected result with lowercase column names
    expected_data = {
        "column1": [1, 2, 3],
        "column2": ["A", "B", "C"]
    }
    expected_df = pl.DataFrame(expected_data)

    # Check if the result matches the expected DataFrame
    assert result_df.frame_equal(expected_df)