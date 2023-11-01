from pendulum import datetime
from loguru import logger

@logger.catch
def get_time_period():
    """
    Return the current year and month as str
    """
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the current date and time to obtain the time period as "YYYY-MM"
    time_period = current_datetime.strftime("%Y_%m")
    logger.info(f"Time period: {time_period}")