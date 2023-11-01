import re
from loguru import logger

@logger.catch
def modify_file_name(name):
    """
    Modify a file name by performing the following transformations:

    Args:
        name (str): The original file name to be modified.

    Returns:
        str: The modified file name.

    Example:
        >>> modify_file_name("My File 123.txt")
        'my_file_123.txt'

        >>> modify_file_name("!@#File Name$%^")
        'file_name'
    """

    # Convert the file name to lowercase
    name = name.lower()

    # Replace non-alphanumeric and non-underscore characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_\.]+', '_', name)

    # Remove non-alphanumeric characters from the start and end of the name
    name = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', name)

    return name
