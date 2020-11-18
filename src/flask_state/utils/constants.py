class OperatingSystem:
    WINDOWS_SYSTEM = "Windows"  # Windows system
    UNIX_SYSTEM = "Unix"  # Unix system


class DBAddressConstants:
    DB_URL_HEADER = "sqlite:///"  # Database URL specification header
    MIN_ADDRESS_LENGTH = 11  # Minimum number of address length


class CronConstants:
    NOT_RANGE_LENGTH = 1  # Do not use the "-" time period divided into length. E.g. "59" -> ["59"]
    IS_RANGE_LENGTH = 2  # Use "-" to split the length of the time period. E.g. "0-59" -> "["0", "59"]"
    SELECT_LAST_TIME_SCALE = 1  # Select the last item in range()
    MIN_ADDRESS_LENGTH = 11  # Minimum number of address length
    NOT_ALLOW_TIME_SCALE = -1  # Maximum time scale not allowed
    NOT_ALLOW_DAY_SCALE = 0  # Maximum days not allowed scale


class TimeConstants:
    SECONDS_TO_MILLISECOND_MULTIPLE = 1000  # Second to millisecond multiple
    ONE_MINUTE_SECONDS = 60
    SOLAR_MONTH_LAST_DAY = 31
    LEAP_YEAR_FEBRUARY_DAY = 29
    AVERAGE_YEAR_FEBRUARY_DAY = 28
    INITIAL_MONTH = 1
    MAX_MONTH = 12
    INITIAL_DAY = 1
    SOLAR = "SOLAR"  # Solar month
    LUNAR = "LUNAR"  # Lunar month


class NumericConstants:
    CARRY = 1
    NO_CARRY = 0
    FOUR_TIMES = 4
    A_HUNDRED_TIMES = 100
    REMAINDER_ZERO = 0  # The remainder is 0
    PERCENTAGE = 100  # Percentage calculation
    INITIAL_INDEX = 0
