from dags.utils.format_url import format_url

def test_format_url():
    # Test case 1: URL with query parameters
    url1 = "https://www.ers.usda.gov/page?q=example"
    expected_output1 = "https://www.ers.usda.gov/page"
    assert format_url(url1) == expected_output1

    # Test case 2: URL without query parameters
    url2 = "https://www.ers.usda.gov/page"
    expected_output2 = "https://www.ers.usda.gov/page"
    assert format_url(url2) == expected_output2

    # Test case 3: URL with http prefix
    url3 = "http://www.ers.usda.gov/page?q=example"
    expected_output3 = "http://www.ers.usda.gov/page"
    assert format_url(url3) == expected_output3

    # Test case 4: URL with https prefix
    url4 = "https://www.example.com/page?q=example"
    expected_output4 = "https://www.example.com/page"
    assert format_url(url4) == expected_output4

    # Test case 5: URL with multiple query parameters
    url5 = "https://www.example.com/page?q1=example1&q2=example2"
    expected_output5 = "https://www.example.com/page"
    assert format_url(url5) == expected_output5