import furl
import re
from loguru import logger

@logger.catch
def format_url(url):
    """
    Format URL

    Args:
        url (str): The original URL to be formatted.

    Returns:
        str: The formatted URL.

    Example:
        >>> format_url("https://www.ers.usda.gov/page?q=example")
        'https://www.ers.usda.gov/page'
    """


    # Define a regular expression pattern to remove query parameters from the URL
    pattern = r'\?.+'

    # Use regular expression substitution to remove the pattern from the URL
    url = re.sub(pattern, '', url)

    # Define a prefix for the URL
    prefix = "https://www.ers.usda.gov"

    # Add prefix if URL does not start with https:// or http://
    if not url.startswith("https://") and not url.startswith("http://"):
        url = furl.furl(prefix).add(path=url).url

    return url