import requests
import datetime
import re

from .mariadb_connector import MariaDBConnector
from ..fldlogging import log
from ..calcs import times


def check_if_entity_name_valid(entity_id: str) -> None:
    if re.match('^[A-Za-z0-9_]+\\.[A-Za-z0-9_]+$', entity_id) is None:
        raise HomeassistantConnectorException('The entity id string is not a valid entity id')


class HomeAssistantConnector:
    _ha_api_url, _ha_api_headers = None, None

    def __init__(self, ha_host: str, ha_port: int, ha_api_token: str, https: bool = False):
        self._ha_api_url = 'http' + ('s' if https else '') + '://' + ha_host + ':' + str(ha_port) + '/api'
        self._ha_api_headers = {
            'Authorization': 'Bearer ' + ha_api_token,
            'Content-Type': 'application/json'
        }

    def get_all_states(self) -> (list[dict], None):
        res = requests.get(self._ha_api_url + '/states', headers=self._ha_api_headers)
        if res.status_code == 200 or res.status_code == 201:
            return res.json()
        else:
            log(error='API-Request status code ' + str(res.status_code))
            return None

    def get_state(self, entity_id: str) -> (dict, None):
        check_if_entity_name_valid(entity_id)

        res = requests.get(self._ha_api_url + '/states/' + entity_id, headers=self._ha_api_headers)
        if res.status_code == 200 or res.status_code == 201:
            return res.json()
        else:
            log(error='API-Request status code ' + str(res.status_code))
            return None

    def post_state(self, entity_id: str, state, attr: dict = None) -> bool:
        check_if_entity_name_valid(entity_id)

        data = {
            'state': str(state)
        }
        if attr is None:
            attr = dict()
        try:
            x = attr['friendly_name']
        except KeyError:
            attr['friendly_name'] = re.match('^[A-Za-z0-9_]+\\.([A-Za-z0-9_]+)$', entity_id).group()
        data['attributes'] = attr
        data = str(data).replace('"', '`').replace("'", '"').encode('utf-8')

        res = requests.post(self._ha_api_url + '/states/' + entity_id, headers=self._ha_api_headers, data=data)
        if res.status_code == 200 or res.status_code == 201:
            return True
        else:
            return False


class HomeAssistantWithDatabaseConnector(HomeAssistantConnector):
    _db = None

    def __init__(self, ha_host: str, ha_port: int, ha_api_token: str, db_host: str, db_port: int, db_database: str,
                 db_user: str, db_password: str):
        super().__init__(ha_host, ha_port, ha_api_token)
        self._db = MariaDBConnector(db_host, db_port, db_database, db_user, db_password)

    def get_min_max_in_interval(self, entity_id: str, from_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), to_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), threshold_including: (int, float) = None, threshold_excluding: (int, float) = None, minimum_true_maximum_false: bool = True, as_utc: bool = False) -> (tuple[float, datetime.datetime], None):
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        check_if_entity_name_valid(entity_id)
        from_utc_timestamp, to_utc_timestamp = times.check_datetime_interval(from_utc_timestamp, to_utc_timestamp, True)

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

        result = self._db.execute_statement(f"SELECT CAST(state AS float) AS state_float, last_updated FROM states WHERE entity_id=? AND last_updated > ? AND last_updated < ? {sql_threshold} ORDER BY state_float {sql_min_max_order} LIMIT 1;", (entity_id, from_utc_timestamp, to_utc_timestamp))
        if not result:
            log(error='DB response is invalid.')
            return None
        return result[0][0], result[0][1] if not as_utc else times.convert_utc_to_cet(result[0][1])

    def get_avg_in_interval(self, entity_id: str, from_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), to_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), threshold_including: (int, float) = None, threshold_excluding: (int, float) = None, minimum_true_maximum_false_threshold: bool = True) -> (float, None):
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        check_if_entity_name_valid(entity_id)
        from_utc_timestamp, to_utc_timestamp = times.check_datetime_interval(from_utc_timestamp, to_utc_timestamp, True)

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

        result = self._db.execute_statement(f"SELECT CAST(state AS float) AS state_float FROM states WHERE entity_id=? AND last_updated > ? AND last_updated < ? {sql_threshold};", (entity_id, from_utc_timestamp, to_utc_timestamp))
        if not result:
            log(error='DB response is invalid.')
            return None
        states_sum = 0
        anz = 0
        for state in result:
            if state[0] != 'unavailable' and state[0] != 'unknown':
                states_sum += state[0]
                anz += 1
        if anz != 0:
            return states_sum / anz
        else:
            return None

    def get_all_states_in_interval(self, entity_id: str, from_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), to_utc_timestamp: datetime.datetime = datetime.datetime.utcnow(), threshold_including: (int, float) = None, threshold_excluding: (int, float) = None, minimum_true_maximum_false_threshold: bool = True, as_utc: bool = False) -> (list[tuple[float, datetime.datetime]], None):
        """
        Standard: From today 00:00:00 to 23:59:59
        """
        check_if_entity_name_valid(entity_id)
        from_utc_timestamp, to_utc_timestamp = times.check_datetime_interval(from_utc_timestamp, to_utc_timestamp, True)

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

        result = self._db.execute_statement(f"SELECT CAST(state AS float) AS state_float, last_updated FROM states WHERE entity_id=? AND last_updated > ? AND last_updated < ? {sql_threshold} ORDER BY last_updated ASC;", (entity_id, from_utc_timestamp, to_utc_timestamp))
        if not result:
            log(error='DB response is invalid.')
            return None

        if as_utc:
            return result
        else:
            list_of_value_pairs = []
            for value_pair in result:
                list_of_value_pairs.append((value_pair[0], times.convert_utc_to_cet(value_pair[1])))
            return list_of_value_pairs


class HomeassistantConnectorException(Exception):
    def __init__(self, text: str):
        super().__init__(text)
