import time

from ..conf.config import MONTH_NAME, TimeScale
from .format_conf import format_cron, format_cron_sec

INITIAL_HOUR_MIN = 0
INITIAL_MONTH_DAY = 1
CARRY = 1
NO_CARRY = 0
MONTH_COUNT = 12
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
    def __init__(self, second="0", minutes="0, 10, 59", hours="0-23", days="1-31"):
        self.second = format_cron_sec(second)
        self.minutes = format_cron((TimeScale.MINUTE.value, minutes))
        self.hours = format_cron((TimeScale.HOUR.value, hours))
        self.days = format_cron((TimeScale.DAY.value, days))
        self.month = int(time.strftime("%m"))
        self.year = int(time.strftime("%y"))
        self.minute_index = 0
        self.hour_index = 0
        self.day_index = 0
        self.max_minute_index = len(self.minutes)
        self.max_hour_index = len(self.hours)
        self.max_day_index = len(self.days)
        self.solar_day_count = SOLAR_MONTH_LAST_DAY
        self.lunar_day_count = LUNAR_MONTH_LAST_DAY
        self.leap_day_count = LEAP_YEAR_FEBRUARY_DAY
        self.average_day_count = AVERAGE_YEAR_FEBRUARY_DAY

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

        hour_carry = CARRY if self.minute_index == INITIAL_HOUR_MIN else NO_CARRY
        if hour_carry:
            self.hour_index = (self.hour_index + hour_carry) % self.max_hour_index

        day_carry = CARRY if hour_carry == CARRY and self.hour_index == INITIAL_HOUR_MIN else NO_CARRY
        if day_carry:
            self.max_day_index = self._get_month_days(self.month, self.year)
            self.day_index = (self.hour_index + day_carry) % self.max_day_index

        month_carry = CARRY if day_carry == CARRY and self.day_index == INITIAL_MONTH_DAY else NO_CARRY
        if month_carry:
            self.month = (self.month + month_carry) % MONTH_COUNT

        year_carry = CARRY if month_carry == CARRY and self.month == INITIAL_MONTH_DAY else NO_CARRY
        if year_carry:
            self.year = self.year + year_carry

    def _get_month_days(self, month, year):
        month_name = MONTH_NAME.get(month)
        if month_name == SOLAR:
            return self.solar_day_count
        elif month_name == LUNAR:
            return self.lunar_day_count
        else:
            if year % FOUR_TIMES == REMAINDER_ZERO and year % A_HUNDRED_TIMES != REMAINDER_ZERO:
                return self.leap_day_count
            else:
                return self.average_day_count
