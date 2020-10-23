import time

from ..conf.config import DAYS_SCOPE, DaysMilliseconds

SECONDS_TO_MILLISECOND_MULTIPLE = 1000  # Second to millisecond multiple


def get_current_ms():
    """
    Return the current millisecond time
    :return: the current millisecond time
    """
    return int(round(time.time() * SECONDS_TO_MILLISECOND_MULTIPLE))


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
    return DaysMilliseconds[DAYS_SCOPE.get(days)].value if days in DAYS_SCOPE else 0
