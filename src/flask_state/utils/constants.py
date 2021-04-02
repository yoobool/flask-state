from enum import Enum, unique


class OperatingSystem:
    WINDOWS_SYSTEM = "Windows"  # Windows system
    UNIX_SYSTEM = "Unix"  # Unix system


class CronConstants:
    NOT_RANGE_LENGTH = 1  # Do not use the "-" time period divided into length. E.g. "59" -> ["59"]
    IS_RANGE_LENGTH = 2  # Use "-" to split the length of the time period. E.g. "0-59" -> "["0", "59"]"
    SELECT_LAST_TIME_SCALE = 1  # Select the last item in range()
    SOLAR_MONTH_LAST_DAY = 31
    LEAP_YEAR_FEBRUARY_DAY = 29
    AVERAGE_YEAR_FEBRUARY_DAY = 28
    INITIAL_MONTH = 1
    MAX_MONTH = 12
    INITIAL_DAY = 1
    SOLAR = "SOLAR"  # Solar month
    LUNAR = "LUNAR"  # Lunar month
    NOT_ALLOW_TIME_SCALE = -1  # Maximum time scale not allowed
    NOT_ALLOW_DAY_SCALE = 0  # Maximum days not allowed scale
    MAX_TIME_SCALE = {"SECOND": 60, "MINUTE": 60, "HOUR": 24, "DAY": 32}  # Maximum time scale
    MONTH_NAME = {
        1: "SOLAR",
        2: "FEBRUARY",
        3: "SOLAR",
        4: "LUNAR",
        5: "SOLAR",
        6: "LUNAR",
        7: "SOLAR",
        8: "SOLAR",
        9: "LUNAR",
        10: "SOLAR",
        11: "LUNAR",
        12: "SOLAR",
    }  # The mean of the month


class TimeConstants:
    SECONDS_TO_MILLISECOND_MULTIPLE = 1000  # Second to millisecond multiple
    FIF_SECOND_TO_MILLSECOND = 15000
    ONE_MINUTE_SECONDS = 60
    DAYS_SCOPE = {
        1: "ONE_DAY",
        3: "THREE_DAY",
        7: "SEVEN_DAY",
        30: "THIRTY_DAY",
    }  # Date selection range


class NumericConstants:
    CARRY = 1
    NO_CARRY = 0
    FOUR_TIMES = 4
    A_HUNDRED_TIMES = 100
    REMAINDER_ZERO = 0  # The remainder is 0
    PERCENTAGE = 100  # Percentage calculation
    INITIAL_INDEX = 0


@unique
class TimeScale(Enum):
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


# Date selection range milliseconds
@unique
class DaysMilliseconds(Enum):
    ONE_DAY = 86400000
    THREE_DAY = 259200000
    SEVEN_DAY = 604800000
    THIRTY_DAY = 2592000000


@unique
class HttpMethod(Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HTTPStatus:
    """Http standard status code"""

    OK = 200
    BAD_REQUEST = 400
    METHOD_NOT_ALLOWED = 405
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500


class LogLevels:
    """Log level"""

    INFO = "INFO"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    EXCEPTION = "EXCEPTION"
    DEFAULT = "INFO"


class AnsiColor:
    """ANSI escape code"""

    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"
