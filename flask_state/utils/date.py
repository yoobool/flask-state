import time


def get_current_ms():
    """
    Return the current millisecond time
    :return: the current millisecond time
    """
    return int(round(time.time() * 1000))


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
    time_stamp = {'1': 86400000, '3': 259200000, '7': 604800000, '30': 2592000000}
    return time_stamp.get(days) or 0
