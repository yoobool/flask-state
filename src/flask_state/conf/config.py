from enum import Enum, unique


# Constant class
class Constant:
    DEFAULT_SECONDS = 60  # Record local state interval
    MIN_SECONDS = 60  # Optional minimum number of seconds
    REDIS_TIMEOUT = 1  # Redis connection timeout
    CPU_PERCENT_INTERVAL = 0  # Time interval to calculate CPU utilization using psutil
    DEFAULT_BIND_SQLITE = 'flask_state_sqlite'  # Default binding database URL key
    DEFAULT_DB_URL = 'sqlite:///flask_state_host.db'  # Default database URL
    WINDOWS_SYSTEM = 'Windows'  # Windows system
    UNIX_SYSTEM = 'Unix'  # Unix system
    MIN_ADDRESS_LENGTH = 11  # Minimum number of address length
    MAX_RETURN_RECORDS = 480  # Return the maximum number of records


# Date selection range
DAYS_SCOPE = {
    1: 'ONE_DAY',
    3: 'THREE_DAY',
    7: 'SEVEN_DAY',
    30: 'THIRTY_DAY',
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
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
