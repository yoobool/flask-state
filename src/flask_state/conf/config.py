from enum import Enum, unique


# Constant class
class Constant:
    DEFAULT_SECONDS = 60  # Record local state interval
    MIN_SECONDS = 10  # Optional minimum number of seconds
    REDIS_TIMEOUT = 1  # Redis connection timeout
    CPU_PERCENT_INTERVAL = 0  # Time interval to calculate CPU utilization using psutil
    DEFAULT_BIND_SQLITE = 'flask_state_sqlite'  # Default binding database URL key
    DEFAULT_DB_URL = 'sqlite:///flask_state_host.db'  # Default database URL
    WINDOWS_SYSTEM = 'Windows'  # Windows system
    UNIX_SYSTEM = 'Unix'  # Unix system
    MIN_ADDRESS_LENGTH = 11  # minimum number of address length


# Date selection range
@unique
class DaysScope(Enum):
    One_Day = 1
    Three_Day = 3
    Seven_Day = 7
    Thirty_Day = 30


# Date selection range milliseconds
@unique
class DaysMilliseconds(Enum):
    One_Day = 86400000
    Three_Day = 259200000
    Seven_Day = 604800000
    Thirty_Day = 2592000000


@unique
class HttpMethod(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


DAYS_SCOPE = dict([(str(DaysScope[key].value), DaysScope[key].value) for key in DaysScope.__members__])

DAYS_SCOPE_MILLISECONDS = dict(
    [(str(DaysScope[key].value), DaysMilliseconds[key].value) for key in DaysMilliseconds.__members__])
