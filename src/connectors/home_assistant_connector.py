import requests
import time
import datetime

import mariadb_connector

class home_assistant_connector():

    def __init__(self):
        pass


class home_assistant_db_connector(home_assistant_connector):

    _db = None

    def __init__(self, db_host: str, db_port: int, db_database: str, db_user: str, db_password: str):
        super().__init__()
        self._db = mariadb_connector.mariadb_connector(db_host, db_port, db_database, db_user, db_password)

    def _convert_utc_to_cet(self, utc_time: datetime.datetime):
        epoch = time.mktime(utc_time.timetuple())
        offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
        return utc_time + offset

    def get_timestamp_of_value_in_intervall(self, from_year: int = -1, from_month: int = -1, from_day: int = -1, from_hour: int = -1, from_minute: int = -1, from_second: int = -1, to_year: int = -1, to_month: int = -1, to_day: int = -1, to_hour: int = -1, to_minute: int = -1, to_second: int = -1, threshold: int = 0, minimum_True_maximum_False: bool = True) -> datetime.datetime:
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        if from_year == -1:
            from_year = int(datetime.datetime.now().year)
        if from_month == -1:
            from_month = int(datetime.datetime.now().month)
        if from_day == -1:
            from_day = int(datetime.datetime.now().day)
        if from_hour == -1:
            from_hour = 0
        if from_minute == -1:
            from_minute = 0
        if from_second == -1:
            from_second = 0
        if to_year == -1:
            to_year = int(datetime.datetime.now().year)
        if to_month == -1:
            to_month = int(datetime.datetime.now().month)
        if to_day == -1:
            to_day = int(datetime.datetime.now().day)
        if to_hour == -1:
            to_hour = 23
        if to_minute == -1:
            to_minute = 59
        if to_second == -1:
            to_second = 59
        # TODO: Check every possible condition, not just days
        if from_year > to_year or (from_year == to_year and from_month > to_month) or (
                from_year == to_year and from_month == to_month and from_day >= to_day):
            """ If from date is after to date """
            print('Error: From date is after to date.')
            return []
        # TODO: Migrate functions from fldsvs

