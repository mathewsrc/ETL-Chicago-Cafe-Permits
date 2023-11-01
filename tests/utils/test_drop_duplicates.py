import polars as pl
from dags.utils.drop_duplicates import drop_duplicates 

def test_drop_duplicates():
    # Create a test DataFrame with duplicates
    test_data = {
        "Column1": [1, 2, 2, 3, 4],
        "Column2": ["A", "B", "B", "C", "D"]
    }
    df = pl.DataFrame(test_data)

    # Call the function to remove duplicates
    result_df = drop_duplicates(df).sort(by="Column1")

    # Define the expected result after removing duplicates
    expected_data = {
        "Column1": [1, 2, 3, 4],
        "Column2": ["A", "B", "C", "D"]
    }
    expected_df = pl.DataFrame(expected_data)

    # Check if the result matches the expected DataFrame
    assert result_df.frame_equal(expected_df)
