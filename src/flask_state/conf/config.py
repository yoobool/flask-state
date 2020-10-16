from enum import Enum, unique

# Record local state interval
DEFAULT_SECONDS = 60

# Redis connection timeout
REDIS_TIMEOUT = 1

# Time interval to calculate CPU utilization using psutil
CPU_PERCENT_INTERVAL = 0


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

