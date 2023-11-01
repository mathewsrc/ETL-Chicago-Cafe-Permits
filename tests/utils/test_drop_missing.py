import polars as pl
from dags.utils.drop_missing import drop_missing  # Replace 'your_module' with the actual module name

def test_drop_missing():
    # Create a test DataFrame with missing values
    test_data = {
        "permit_number": [1, 2, None, 4, 5],
        "city": ["New York", "Los Angeles", "Chicago", None, "Miami"],
        "legal_name": ["ABC Inc.", "XYZ Corp.", None, "LMN Ltd.", "PQR Co."],
        "doing_business_as_name": ["ABC", "XYZ", "DEF", None, "PQR"]
    }
    df = pl.DataFrame(test_data)

    # Call the function to remove rows with missing values
    result_df = drop_missing(df)

    # Define the expected result without rows containing missing values
    expected_data = {
        "permit_number": [1, 2, 5],
        "city": ["New York", "Los Angeles", "Miami"],
        "legal_name": ["ABC Inc.", "XYZ Corp.", "PQR Co."],
        "doing_business_as_name": ["ABC", "XYZ", "PQR"]
    }
    expected_df = pl.DataFrame(expected_data)

    # Check if the result matches the expected DataFrame
    assert result_df.frame_equal(expected_df)
