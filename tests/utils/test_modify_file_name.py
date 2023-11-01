import pytest
from dags.utils.modify_file_name import modify_file_name  # Replace 'your_module' with the actual module name

def test_modify_file_name():
    # Test with valid file names
    assert modify_file_name("My File 123.txt") == 'my_file_123.txt'
    assert modify_file_name("!@#File Name$%^") == 'file_name'
    assert modify_file_name("Another Example 456.file") == 'another_example_456.file'

    # Test with empty file name
    assert modify_file_name("") == ''

    # Test with file names that become empty after transformation
    assert modify_file_name("!@#$%^") == ''

    # Test with file names containing only digits
    assert modify_file_name("1234567890") == '1234567890'

    # Test with file names containing only non-alphanumeric characters
    assert modify_file_name("@#$%^&*()") == ''