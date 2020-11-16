from enum import Enum, unique


# Constant class
class Constant:
    DEFAULT_SECONDS = 60  # Record local state interval
    MIN_SECONDS = 60  # Optional minimum number of seconds
    REDIS_TIMEOUT = 1  # Redis connection timeout
    CPU_PERCENT_INTERVAL = 0  # Time interval to calculate CPU utilization using psutil
    DEFAULT_BIND_SQLITE = "flask_state_sqlite"  # Default binding database URL key
    DEFAULT_DB_URL = "sqlite:///flask_state_host.db"  # Default database URL
    WINDOWS_SYSTEM = "Windows"  # Windows system
    UNIX_SYSTEM = "Unix"  # Unix system
    MIN_ADDRESS_LENGTH = 11  # Minimum number of address length
    MAX_RETURN_RECORDS = 480  # Return the maximum number of records
    MIN_TIME_SCALE = -1  # Minimum time scale
    MIN_DAY_SCALE = 0  # Minimum day scale


@unique
class TimeScale(Enum):
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


# Maximum time scale
MAX_TIME_SCALE = {"SECOND": 60, "MINUTE": 60, "HOUR": 24, "DAY": 32}

# The mean of the month
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
}

# Date selection range
DAYS_SCOPE = {
    1: "ONE_DAY",
    3: "THREE_DAY",
    7: "SEVEN_DAY",
    30: "THIRTY_DAY",
}


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
