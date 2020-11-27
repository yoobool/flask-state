import time

from .constants import DaysMilliseconds, TimeConstants


def get_current_ms():
    """
    Return the current millisecond time
    :return: the current millisecond time
    """
    return int(round(time.time() * TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE))


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
    days_scope = TimeConstants.DAYS_SCOPE
    return DaysMilliseconds[days_scope.get(days)].value if days in days_scope else 0


def get_formatted_timestamp(timestamp):
    """
    Get formatted timestamp
    :param timestamp:
    :return: formatted timestamp
    :rtype: str
    """
    time_local = time.localtime(timestamp)
    format_date = time.strftime("%Y_%m_%d %H:%M:%S", time_local)
    return format_date
