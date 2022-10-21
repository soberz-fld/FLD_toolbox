import datetime
import time

def convert_utc_to_cet(self, utc_time: datetime.datetime):
    epoch = time.mktime(utc_time.timetuple())
    offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
    return utc_time + offset


def get_next_day_as_ints(self, p_year: int, p_month: int, p_day: int):
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


def calculate_if_year_is_leapyear(self, p_year: int) -> bool:
    schalt = False
    if p_year % 4 == 0:
        schalt = True
    if p_year % 100 == 0:
        schalt = False
    if p_year % 400 == 0:
        schalt = True
    return schalt
