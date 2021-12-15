from datetime import datetime, timedelta
import re


class _TimeExpression:
    time_regex = re.compile(r"^(\d+,|\d+-\d+,)*(\d+|\d+-\d+)$")

    def __init__(self, range_str: str):
        res = self.time_regex.fullmatch(range_str)
        if not res or not self.check_range(range_str):
            raise ValueError("The cron expression does not conform to the specification. Use default interval.")

    def check_range(self, range_str) -> bool:
        rlist = map(int, re.split(',|-', range_str))
        tmp = self.min - 1
        for r in rlist:
            if r > self.max or r <= tmp:
                return False
            tmp = r
        return True


class HourExpression(_TimeExpression):
    min = 0
    max = 23

    def __init__(self, range_str):
        super(HourExpression, self).__init__(range_str=range_str)


class MinuteExpression(_TimeExpression):
    min = 0
    max = 59

    def __init__(self, range_str):
        super(MinuteExpression, self).__init__(range_str=range_str)


class Cron:
    hour = [*range(24)]
    minute = [*range(60)]
    minute_index = 0
    hour_index = 0

    def __init__(self, hour: str = None, minute: str = None):
        if not hour:
            self.hour = self.make_time(hour)
        if not minute:
            self.minute = self.make_time(minute)

    @staticmethod
    def make_time(time_str: str):
        res = [int]
        time_list = time_str.split(",")
        for t in time_list:
            r = t.split("-")
            if len(r) == 2:
                res.extend([num for num in range(int(r[0]), int(r[1]) + 1)])
            else:
                res.append(int(r[0]))
        return res

    def get_first_wait_time(self):
        now_datetime = datetime.now()
        now_min = now_datetime.minute
        now_hour = now_datetime.hour
        carrier = 0
        for i, m in enumerate(self.minute):
            if m > now_min:
                new_min = m
                self.minute_index = i
                break
        else:
            new_min = self.minute[0]
            carrier = 1

        for i, h in enumerate(self.hour):
            if now_hour + carrier <= h:
                new_hour = h
                self.hour_index = i
                carrier = 0
                break
        else:
            new_hour = self.hour[0]

        new_datetime = now_datetime.replace(hour=new_hour, minute=new_min) + timedelta(days=carrier)
        timestamp_delta = new_datetime.timestamp() - now_datetime.timestamp()
        return timestamp_delta

    def get_next_wait_time(self):
        now_datetime = datetime.now()
        carrier = 0
        if self.minute_index == len(self.minute):
            new_minute = self.minute[0]
            self.minute_index = 0
            carrier = 1
        else:
            new_minute = self.minute[self.minute_index]
            self.minute_index += 1

        new_hour = self.hour[self.hour_index]
        if carrier:
            if self.hour_index == len(self.hour):
                new_hour = self.hour[0]
                self.hour_index = 0
            else:
                self.hour_index += 1
                carrier = 0

        new_datetime = now_datetime.replace(hour=new_hour, minute=new_minute) + timedelta(days=carrier)
        timestamp_delta = new_datetime.timestamp() - now_datetime.timestamp()
        return timestamp_delta
