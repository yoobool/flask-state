# Record local state interval
Default_Seconds = 60

# Redis connection timeout
Redis_Timeout = 1

# Time interval to calculate CPU utilization using psutil
CPU_Percent_Interval = 0


# Date selection range
class DaysScope:
    One_Day = 1
    Three_Day = 3
    Seven_Day = 7
    Thirty_Day = 30


# Date selection range milliseconds
class DaysMilliseconds:
    One_Day = 86400000
    Three_Day = 259200000
    Seven_Day = 604800000
    Thirty_Day = 2592000000


DAYS_SCOPE = {str(DaysScope.One_Day): DaysScope.One_Day,
              str(DaysScope.Three_Day): DaysScope.Three_Day,
              str(DaysScope.Seven_Day): DaysScope.Seven_Day,
              str(DaysScope.Thirty_Day): DaysScope.Thirty_Day}

DAYS_SCOPE_Milliseconds = {str(DaysScope.One_Day): DaysMilliseconds.One_Day,
                           str(DaysScope.Three_Day): DaysMilliseconds.Three_Day,
                           str(DaysScope.Seven_Day): DaysMilliseconds.Seven_Day,
                           str(DaysScope.Thirty_Day): DaysMilliseconds.Thirty_Day}
