import time
from bisect import bisect_left, bisect_right

from ..conf.config import MONTH_NAME, TimeScale
from .format_conf import format_cron, format_cron_sec

INITIAL_INDEX = 0
INITIAL_HOUR_MIN = 0
INITIAL_MONTH_DAY = 1
CARRY = 1
NO_CARRY = 0
MAX_MONTH = 12
SOLAR_MONTH_LAST_DAY = 31
LUNAR_MONTH_LAST_DAY = 30
LEAP_YEAR_FEBRUARY_DAY = 28
AVERAGE_YEAR_FEBRUARY_DAY = 29
SOLAR = "SOLAR"  # Solar month
LUNAR = "LUNAR"  # Lunar month
FOUR_TIMES = 4
A_HUNDRED_TIMES = 100
REMAINDER_ZERO = 0


class Cron:
    def __init__(self, second="0", minutes="0-59", hours="0-23", days="1-31"):
        self.second = format_cron_sec(second)
        self.minutes = format_cron((TimeScale.MINUTE.value, minutes))
        self.hours = format_cron((TimeScale.HOUR.value, hours))
        self.days = format_cron((TimeScale.DAY.value, days))

        self.max_minute_index = len(self.minutes)
        self.max_hour_index = len(self.hours)

        self.solar_day_count = SOLAR_MONTH_LAST_DAY
        self.lunar_day_count = LUNAR_MONTH_LAST_DAY
        self.leap_day_count = LEAP_YEAR_FEBRUARY_DAY
        self.average_day_count = AVERAGE_YEAR_FEBRUARY_DAY
        self.max_day_index = self._get_max_day_index(int(time.strftime("%m")), int(time.strftime("%y")))
        self.year, self.month, self.day_index, self.hour_index, self.minute_index = self._get_initial_index()

    def get(self):
        target_time_stamp = time.mktime(
            time.strptime(
                "{}-{}-{} {}:{}:{}".format(
                    self.year,
                    self.month,
                    self.days[self.day_index],
                    self.hours[self.hour_index],
                    self.minutes[self.minute_index],
                    self.second,
                ),
                "%Y-%m-%d %H:%M:%S",
            )
        )
        self._update_index()
        return target_time_stamp

    def _update_index(self):
        self.minute_index = (self.minute_index + CARRY) % self.max_minute_index

        hour_carry = CARRY if self.minute_index == INITIAL_INDEX else NO_CARRY
        if hour_carry:
            self.hour_index = (self.hour_index + hour_carry) % self.max_hour_index

        day_carry = CARRY if hour_carry == CARRY and self.hour_index == INITIAL_INDEX else NO_CARRY

        if day_carry:
            self.max_day_index = self._get_max_day_index(self.month, self.year)
            self.day_index = (self.day_index + day_carry) % self.max_day_index

        month_carry = CARRY if day_carry == CARRY and self.day_index == INITIAL_INDEX else NO_CARRY

        if month_carry:
            new_month = self.month + month_carry
            self.month = INITIAL_MONTH_DAY if new_month > MAX_MONTH else new_month

        year_carry = CARRY if month_carry == CARRY and self.month == INITIAL_MONTH_DAY else NO_CARRY
        if year_carry:
            self.year = self.year + year_carry

    def _get_max_day_index(self, month, year):
        month_name = MONTH_NAME.get(month)
        if month_name == SOLAR:
            position = bisect_left(self.days, self.solar_day_count)
            return position if self.days[position] + 1 != self.solar_day_count else position + 2
        elif month_name == LUNAR:
            position = bisect_left(self.days, self.lunar_day_count)
            return position if self.days[position] + 1 != self.lunar_day_count else position + 2
        else:
            if year % FOUR_TIMES == REMAINDER_ZERO and year % A_HUNDRED_TIMES != REMAINDER_ZERO:
                position = bisect_left(self.days, self.leap_day_count)
                return position if self.days[position] + 1 != self.leap_day_count else position + 2
            else:
                position = bisect_left(self.days, self.average_day_count)
                return position if self.days[position] + 1 != self.average_day_count else position + 2

    def _get_initial_index(self):
        _year, _month, _day, _hour, _minute = map(int, time.strftime("%Y,%m,%d,%H,%M").split(","))

        minute_position = bisect_right(self.minutes, _minute)
        hour_carry, minute_index = (
            (CARRY, INITIAL_INDEX) if minute_position == self.max_minute_index else (NO_CARRY, minute_position)
        )

        hour_position = bisect_left(self.hours, _hour + hour_carry)
        day_carry, hour_index = (
            (CARRY, INITIAL_INDEX) if hour_position == self.max_hour_index else (NO_CARRY, hour_position)
        )

        day_position = bisect_left(self.days, _day + day_carry)
        month_carry, day_index = (
            (CARRY, INITIAL_INDEX) if day_position == self.max_day_index else (NO_CARRY, day_position)
        )

        year_carry, month_index = (
            (CARRY, INITIAL_MONTH_DAY) if month_carry and _month == MAX_MONTH else (NO_CARRY, _month + month_carry)
        )

        year_index = _year + CARRY if year_carry else _year

        if year_carry:
            minute_index, hour_index, day_index, month_index = (
                INITIAL_INDEX,
                INITIAL_INDEX,
                INITIAL_INDEX,
                INITIAL_INDEX,
            )
        elif month_carry:
            minute_index, hour_index, day_index = INITIAL_INDEX, INITIAL_INDEX, INITIAL_INDEX
        elif day_carry:
            minute_index, hour_index = INITIAL_INDEX, INITIAL_INDEX
        elif hour_carry:
            month_index = INITIAL_INDEX
        return year_index, month_index, day_index, hour_index, minute_index
