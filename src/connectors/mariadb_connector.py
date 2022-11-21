import sys
import mariadb


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
            print(e)
            sys.exit()

    def execute_statement(self, statement: str, parameter: tuple = None) -> list:
        self._cursor.execute(statement, parameter)
        result = self._cursor.fetchall()
        if result:
            return result
        else:
            return []
