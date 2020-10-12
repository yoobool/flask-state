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


DAYS_SCOPE = {str(DaysScope.One_Day.value): DaysScope.One_Day.value,
              str(DaysScope.Three_Day.value): DaysScope.Three_Day.value,
              str(DaysScope.Seven_Day.value): DaysScope.Seven_Day.value,
              str(DaysScope.Thirty_Day.value): DaysScope.Thirty_Day.value}

DAYS_SCOPE_MILLISECONDS = {str(DaysScope.One_Day.value): DaysMilliseconds.One_Day.value,
                           str(DaysScope.Three_Day.value): DaysMilliseconds.Three_Day.value,
                           str(DaysScope.Seven_Day.value): DaysMilliseconds.Seven_Day.value,
                           str(DaysScope.Thirty_Day.value): DaysMilliseconds.Thirty_Day.value}
