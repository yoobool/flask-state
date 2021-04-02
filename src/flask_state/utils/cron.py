import time
from bisect import bisect_left, bisect_right

from .constants import CronConstants, NumericConstants, TimeScale
from .format_conf import format_cron, format_cron_sec


class Cron:
    def __init__(self, second="0", minutes="0-59", hours="0-23", days="1-31"):
        self.second = format_cron_sec(second)
        self.minutes = format_cron((TimeScale.MINUTE.value, minutes))
        self.hours = format_cron((TimeScale.HOUR.value, hours))
        self.days = format_cron((TimeScale.DAY.value, days))

        self.max_minute_index = len(self.minutes)
        self.max_hour_index = len(self.hours)

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
        carry = NumericConstants.CARRY
        no_carry = NumericConstants.NO_CARRY
        initial_index = NumericConstants.INITIAL_INDEX
        initial_month = CronConstants.INITIAL_MONTH

        self.minute_index = (self.minute_index + carry) % self.max_minute_index
        hour_carry = carry if self.minute_index == initial_index else no_carry
        if hour_carry:
            self.hour_index = (self.hour_index + hour_carry) % self.max_hour_index

        day_carry = carry if hour_carry == carry and self.hour_index == initial_index else no_carry

        if day_carry:
            self.max_day_index = self._get_max_day_index(self.month, self.year)
            self.day_index = (self.day_index + day_carry) % self.max_day_index

        month_carry = carry if day_carry == carry and self.day_index == initial_index else no_carry

        if month_carry:
            new_month = self.month + month_carry
            self.month = initial_month if new_month > CronConstants.MAX_MONTH else new_month

        year_carry = carry if month_carry == carry and self.month == initial_month else no_carry
        if year_carry:
            self.year = self.year + year_carry

    def _get_max_day_index(self, month, year):
        month_name = CronConstants.MONTH_NAME.get(month)
        common_max_index = len(self.days)
        if month_name == CronConstants.SOLAR:
            return common_max_index
        elif month_name == CronConstants.LUNAR:
            return common_max_index if self.days[-1] < CronConstants.SOLAR_MONTH_LAST_DAY else common_max_index - 1
        else:
            if (
                year % NumericConstants.FOUR_TIMES == NumericConstants.REMAINDER_ZERO
                and year % NumericConstants.A_HUNDRED_TIMES != NumericConstants.REMAINDER_ZERO
            ):
                # Determine whether this year is a leap year
                return (
                    common_max_index
                    if self.days[-1] < CronConstants.LEAP_YEAR_FEBRUARY_DAY
                    else bisect_right(self.days, CronConstants.LEAP_YEAR_FEBRUARY_DAY)
                )
            else:
                return (
                    common_max_index
                    if self.days[-1] < CronConstants.AVERAGE_YEAR_FEBRUARY_DAY
                    else bisect_right(self.days, CronConstants.AVERAGE_YEAR_FEBRUARY_DAY)
                )

    def _get_initial_index(self):
        _year, _month, _day, _hour, _minute = map(int, time.strftime("%Y,%m,%d,%H,%M").split(","))
        carry = NumericConstants.CARRY
        no_carry = NumericConstants.NO_CARRY
        initial_index = NumericConstants.INITIAL_INDEX
        initial_month = CronConstants.INITIAL_MONTH

        minute_position = bisect_right(self.minutes, _minute)
        hour_carry, minute_index = (
            (carry, initial_index) if minute_position == self.max_minute_index else (no_carry, minute_position)
        )

        hour_position = bisect_left(self.hours, _hour + hour_carry)
        day_carry, hour_index = (
            (carry, initial_index) if hour_position == self.max_hour_index else (no_carry, hour_position)
        )

        day_position = bisect_left(self.days, _day + day_carry)
        month_carry, day_index = (
            (carry, initial_index) if day_position == self.max_day_index else (no_carry, day_position)
        )

        year_carry, month = (
            (carry, initial_month)
            if month_carry and _month == CronConstants.MAX_MONTH
            else (no_carry, _month + month_carry)
        )

        year = _year + carry if year_carry else _year

        if year_carry:
            minute_index, hour_index, day_index, month = (
                initial_index,
                initial_index,
                initial_index,
                initial_index,
            )
        elif month_carry:
            minute_index, hour_index, day_index = initial_index, initial_index, initial_index
        elif day_carry:
            minute_index, hour_index = initial_index, initial_index
        elif hour_carry:
            month = initial_index
        return year, month, day_index, hour_index, minute_index
