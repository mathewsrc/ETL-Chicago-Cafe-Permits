import polars as pl
from dags.utils.drop_full_null_columns import drop_full_null_columns  # Replace 'your_module' with the actual module name

def test_drop_full_null_columns():
    # Create a test DataFrame
    test_data = {
        "A": [None, None, None],
        "B": [1, None, 3],
        "C": [4, 5, 6],
    }
    df = pl.DataFrame(test_data)

    # Call the function to drop columns with all-null values
    result_df = drop_full_null_columns(df)

    # Define the expected result
    expected_data = {
        "B": [1, None, 3],
        "C": [4, 5, 6],
    }
    expected_df = pl.DataFrame(expected_data)

    # Check if the result matches the expected DataFrame
    assert result_df.frame_equal(expected_df)
