import datetime
import time

def convert_utc_to_cet(utc_time: datetime.datetime) -> datetime.datetime:
    epoch = time.mktime(utc_time.timetuple())
    offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
    return utc_time + offset

def convert_cet_to_utc(cet_time: datetime.datetime) -> datetime.datetime:
    epoch = time.mktime(cet_time.timetuple())
    offset = datetime.datetime.utcfromtimestamp(epoch) - datetime.datetime.fromtimestamp(epoch)
    return cet_time + offset


def get_next_day_as_ints(p_year: int, p_month: int, p_day: int) -> tuple[int, int, int]:
    if p_year < 1900 or p_month < 1 or p_month > 12 or p_day < 1 or p_day > 31:
        print('Error: get_next_day_as_ints - invalid date')
    else:
        # last day of year
        if p_day == 31 and p_month == 12:
            return p_year + 1, 1, 1
        # Can't be last day
        elif p_day < 28:
            return p_year, p_month, p_day + 1
        # Can't be last day in month with up to 30 days
        elif p_month != 2 and p_day < 30:
            return p_year, p_month, p_day + 1
        # Can't be last day in month with up to 31 days
        elif p_month != 2 and p_month != 4 and p_month != 6 and p_month != 9 and p_month != 11 and p_day < 31:
            return p_year, p_month, p_day + 1
        # End of february
        elif p_month == 2:
            if self.calculate_if_year_is_leapyear(p_year) and p_day == 28:
                return p_year, p_month, 29
            else:
                return p_year, 3, 1
        # End of 30 day long months
        elif p_day == 30 and (p_month == 4 or p_month == 6 or p_month == 9 or p_month == 11):
            return p_year, p_month + 1, 1
        # End of other months
        elif p_day == 31:
            return p_year, p_month + 1, 1
        # Else???
        else:
            print('Error: get_next_day_as_ints - out of handling conditions')


def calculate_if_year_is_leapyear(p_year: int) -> bool:
    schalt = False
    if p_year % 4 == 0:
        schalt = True
    if p_year % 100 == 0:
        schalt = False
    if p_year % 400 == 0:
        schalt = True
    return schalt

def check_datetime_intervall(from_datetime: datetime.datetime, to_datetime: datetime.datetime, use_utc: bool = False) -> tuple[datetime.datetime, datetime.datetime]:
    """
    If identical: From 00:00:00 to 23:59:59 (matching cet even if time is given in utc)
    If to_datetime is before from_datetime: Fixes order
    """
    if (to_datetime - from_datetime).total_seconds() < 0:  # If from date is after to date
        return to_datetime, from_datetime
    if from_datetime == to_datetime:
        if use_utc:
            from_cet = convert_utc_to_cet(from_datetime)
            to_cet = convert_utc_to_cet(to_datetime)
            from_cet_datetime = datetime.datetime(from_cet.year, from_cet.month, from_cet.day, 0, 0, 000000)
            to_cet_datetime = datetime.datetime(to_cet.year, to_cet.month, to_cet.day, 23, 59, 59, 999999)
            from_datetime = convert_cet_to_utc(from_cet_datetime)
            to_datetime = convert_cet_to_utc(to_cet_datetime)
        else:
            from_datetime = datetime.datetime(from_datetime.year, from_datetime.month, from_datetime.day, 0, 0, 000000)
            to_datetime = datetime.datetime(to_datetime.year, to_datetime.month, to_datetime.day, 23, 59, 59, 999999)
    return from_datetime, to_datetime

def get_datetime_from_date(date: datetime.date) -> datetime.datetime:
    return datetime.datetime(date.year, date.month, date.day, 0, 0, 0, 000000)