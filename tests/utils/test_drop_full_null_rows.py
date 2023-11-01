import polars as pl
from dags.utils.drop_full_null_rows import drop_full_null_rows  # Replace 'your_module' with the actual module name

def test_drop_full_null_rows():
    # Create a test DataFrame
    test_data = {
        "A": [None, None, 7],
        "B": [1, None, 3],
        "C": [4, None, None],
    }
    df = pl.DataFrame(test_data)

    # Call the function to drop rows with all-null values
    result_df = drop_full_null_rows(df)

    # Define the expected result
    expected_data = {
        "A": [None, 7],
        "B": [1, 3],
        "C": [4, None],
    }
    expected_df = pl.DataFrame(expected_data)
    
    print(result_df)
    
    print(expected_df)

    # Check if the result matches the expected DataFrame
    assert result_df.frame_equal(expected_df)

