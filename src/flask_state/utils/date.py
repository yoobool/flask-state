import time
from ..conf.config import DAYS_SCOPE_Milliseconds

Seconds_To_Millisecond_Multiple = 1000  # Second to millisecond multiple


def get_current_ms():
    """
    Return the current millisecond time
    :return: the current millisecond time
    """
    return int(round(time.time() * Seconds_To_Millisecond_Multiple))


def get_current_s():
    """
    Returns the current time in seconds
    :return: the current time in seconds
    """
    return int(round(time.time()))


def get_query_ms(days):
    """
    Returns a limited time period of milliseconds
    :param days: query limited days
    :return: a limited time period of milliseconds
    """
    if not isinstance(days, str):
        days = str(days)
    return DAYS_SCOPE_Milliseconds.get(days) or 0
