import sys
import mariadb

from ..fldlogging import log

class MariaDBConnector:
    _conn = None
    _cursor = None

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        try:
            self._conn = mariadb.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self._cursor = self._conn.cursor()
        except mariadb.Error as e:
            log(critical=str(e))
            sys.exit()

    def execute_statement(self, statement: str, parameter: tuple = None, return_column_headers: bool = False) -> list:
        self._cursor.execute(statement, parameter)
        result = self._cursor.fetchall()
        if return_column_headers:
            columns = tuple([desc[0] for desc in self._cursor.description])
            result.insert(0, columns)
        if result:
            return result
        else:
            return []
