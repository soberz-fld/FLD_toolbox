import requests
import time
import datetime

from .mariadb_connector import MariaDBConnector
from ..fldlogging import log
from ..calcs.times import check_datetime_intervall


class HomeAssistantConnector:

    def __init__(self):
        pass


class HomeAssistantWithDatabaseConnector(HomeAssistantConnector):
    _db = None

    def __init__(self, db_host: str, db_port: int, db_database: str, db_user: str, db_password: str):
        super().__init__()
        self._db = MariaDBConnector(db_host, db_port, db_database, db_user, db_password)

    def get_min_max_in_interval(self, entity_id: str, from_timestamp: datetime.datetime = datetime.datetime.now(),
                                to_timestamp: datetime.datetime = datetime.datetime.now(),
                                threshold_including: (int, float) = None, threshold_excluding: (int, float) = None,
                                minimum_true_maximum_false: bool = True) -> (tuple[float, datetime.datetime], None):
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        from_timestamp, to_timestamp = check_datetime_intervall(from_timestamp, to_timestamp)

        # Conditions
        sql_threshold = ''
        sql_min_max_order = ''
        if minimum_true_maximum_false:
            sql_min_max_order = 'ASC'
            if threshold_including is not None:
                sql_threshold = 'AND CAST(state AS float) >= ' + str(threshold_including)
            if threshold_excluding is not None:
                sql_threshold = 'AND CAST(state AS float) > ' + str(threshold_excluding)
        else:
            sql_min_max_order = 'DESC'
            if threshold_including is not None:
                sql_threshold = 'AND CAST(state AS float) <= ' + str(threshold_including)
            if threshold_excluding is not None:
                sql_threshold = 'AND CAST(state AS float) < ' + str(threshold_excluding)

        result = self._db.execute_statement(
            f"SELECT CAST(state AS float) AS state_float, last_updated FROM states WHERE entity_id=? AND last_updated > ? AND last_updated < ? {sql_threshold} ORDER BY state_float {sql_min_max_order} LIMIT 1;",
            (entity_id, from_timestamp, to_timestamp))
        print(result)
        if not result:
            log(error='DB response is invalid.')
            return None
        return result[0][0], result[0][1]

    def get_avg_in_interval(self, entity_id: str, from_timestamp: datetime.datetime = datetime.datetime.now(),
                            to_timestamp: datetime.datetime = datetime.datetime.now(),
                            threshold_including: (int, float) = None, threshold_excluding: (int, float) = None,
                            minimum_true_maximum_false_threshold: bool = True) -> (float, None):
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        from_timestamp, to_timestamp = check_datetime_intervall(from_timestamp, to_timestamp)

        # Conditions
        sql_threshold = ''
        if threshold_including is not None or threshold_excluding is not None:
            if minimum_true_maximum_false_threshold:
                if threshold_including is not None:
                    sql_threshold = 'AND CAST(state AS float) >= ' + str(threshold_including)
                if threshold_excluding is not None:
                    sql_threshold = 'AND CAST(state AS float) > ' + str(threshold_excluding)
            else:
                if threshold_including is not None:
                    sql_threshold = 'AND CAST(state AS float) <= ' + str(threshold_including)
                if threshold_excluding is not None:
                    sql_threshold = 'AND CAST(state AS float) < ' + str(threshold_excluding)

        result = self._db.execute_statement(
            f"SELECT CAST(state AS float) AS state_float FROM states WHERE entity_id=? AND last_updated > ? AND last_updated < ? {sql_threshold};",
            (entity_id, from_timestamp, to_timestamp))
        if not result:
            log(error='DB response is invalid.')
            return None

        value_type = float if '.' in result[0][0] else int
        sum = 0
        anz = 0
        for state in result:
            if state[0] != 'unavailable' and state[0] != 'unknown':
                sum += value_type(state[0])
                anz += 1
        if anz != 0:
            return sum / anz
        else:
            return None
