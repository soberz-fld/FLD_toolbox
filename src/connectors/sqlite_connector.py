import time

from ..fldlogging import log
import sqlite3
import os
import errno
import pathlib

_opened_database_files = list()


class SqliteConnector:
    _database_path: str = None  # The path of the database file
    _database_name: str = None  # The name of the database
    _conn = None  # database connection
    _cursor = None  # database cursor. Used for executes etc
    _committer_free: bool = True  # If file is free to commit, False if some instance is writing

    def __init__(self, database: str = 'database.sqlite3', create_new_if_not_existing: bool = False, sql_script_if_creating_new: str = ''):
        """
        Connector for handling access to SQLite database. Keep in mind that there will be an error if the database file does not exist, and you do not with to create a new one.
        :param database: path to database
        :param create_new_if_not_existing: If the database should be created if not existing with the sql_script
        :param sql_script_if_creating_new: SQL script to be executed if database doesn't exist
        """
        self._database_path = database
        self._database_name = pathlib.PurePath(database).name

        if not os.path.isfile(self._database_path):  # If database file does not exist...
            if create_new_if_not_existing:  # ...test if a new one should be created ...

                # First check if folder exists and create new if not
                os.makedirs(os.path.dirname(self._database_path), exist_ok=True)

                # Open database
                self._conn = sqlite3.connect(self._database_path)

                try:
                    # Create cursor
                    self._cursor = self._conn.cursor()

                    # Initialize database
                    self._create_dbaccess_table()
                    self._cursor.executescript(sql_script_if_creating_new)

                    log(action='Database ' + str(self._database_path) + ' created and initialized')

                except sqlite3.Error:  # If sqlite error occurs: Remove uninitialized database and close connection
                    os.remove(self._database_path)
                    self._conn.close()
                    raise

            else:  # ... else a error must be raised that there is no file
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), database)
        else:  # If database file exists
            # Open database
            self._conn = sqlite3.connect(self._database_path)

            try:
                # Create cursor
                self._cursor = self._conn.cursor()

                # Check if dbaccess exists
                try:
                    self._cursor.execute('SELECT * FROM dbaccess ORDER BY id DESC LIMIT 1;').fetchone()
                except sqlite3.OperationalError as e:
                    if str(e) == 'no such table: dbaccess':  # If table dbaccess does not exist ...
                        self._create_dbaccess_table()  # ...create it
                    else:  # Some other error
                        raise

                # Connection established

            except sqlite3.Error:  # If sqlite error occurs: Close connection
                self._conn.close()
                raise

        # adding it to the static list of opened database files
        _opened_database_files.append(self._database_path)
        log(action='Database ' + self._database_name + ' opened')

    def __del__(self):
        # Closing connection
        try:
            self._conn.close()
        except AttributeError as e:
            if not str(e) == "'NoneType' object has no attribute 'close'":  # if self._conn was null, no connection can be closed of course
                raise
        except sqlite3.ProgrammingError as e:
            if not 'SQLite objects created in a thread can only be used in that same thread. The object was created in thread id' in str(e):
                raise
        # Logging the closing
        try:
            log(action='Database ' + self._database_path + ' closed')
        except NameError as e:
            if str(e) == "name 'open' is not defined":
                pass
            else:
                raise e from None

    def __str__(self):  # Giving more information when printing object information
        return str(self.__repr__()) + ' handling database file ' + str(self._database_path)

    def close(self):
        """
        Closing the database the safe way
        """
        self.__del__()

    def _create_dbaccess_table(self):
        self._cursor.executescript('CREATE TABLE dbaccess ('
                                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                                   'timestamp_utc DATETIME DEFAULT CURRENT_TIMESTAMP,'
                                   'function TEXT NOT NULL,'
                                   'statement TEXT'
                                   ');'
                                   'INSERT INTO dbaccess (function) VALUES ("CREATE");')

    def exe_sql(self, sql: str, parameters: (dict, enumerate) = (), expect_exactly_one_value: bool = False):
        """
        Execute a sql line
        :param sql: SQL statement to execute
        :param parameters: Values inserted for placeholder '?' in statement
        :param expect_exactly_one_value: If true and only one value is given, the value is directly given instead of a list or tuple
        :return: Either none or a value or a list/tuple of values
        """
        try:
            self._cursor.execute(sql, parameters)
            result = self._cursor.fetchall()
        except sqlite3.Error as e:
            log(error='SQL execution error <' + str(e) + '> when executing following statement with parameters: ' + sql + ' | ' + str(parameters))
            raise

        # Log it
        statement = sql if parameters == () else sql + ' | ' + str(parameters)
        try:
            self._cursor.execute('INSERT INTO dbaccess (function, statement) VALUES ("-", ?);', (statement,))
        except sqlite3.Error:
            log(error='Could not log access to database at ' + str(time.time()) + ' with statement ' + statement)

        # Commit changes to the database file
        while not self._committer_free:
            time.sleep(1)
        self._committer_free = False
        self._conn.commit()
        self._committer_free = True

        # Often results of fetchall are gives as list or list of tuple even when there is just one element
        if expect_exactly_one_value:
            if type(result) == list:
                if len(result) == 1:
                    result = result[0]
                    if type(result) == tuple:
                        if len(result) == 1:
                            result = result[0]

        return result
