from pyodbc import Connection


class Loader:

    def __init__(self,
                 connection: Connection):
        self.connection = connection

    def load(self, data: list[tuple]):
        pass

    def _execute_sql(self, sql, params):
        cursor = self.connection.cursor()
        cursor.executemany(sql, params)
        self.connection.commit()
        cursor.close()