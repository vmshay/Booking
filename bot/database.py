import mysql.connector
from bot import config as conf


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host=conf.DB_HOST,
                                                      user=conf.DB_USER,
                                                      password=conf.DB_PASS,
                                                      database=conf.DB_NAME)
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        return self.cursor.execute(sql, params or ())

    def sql_fetchone(self, sql: str):
        self.execute(sql)
        response = self.fetchone()
        if response is None:
            return 'None'
        else:
            for v in response.values():
                return v

    def sql_fetchall(self, sql: str):
        self.execute(sql)
        response = self.fetchall()
        return response

    def sql_query_send(self, sql: str):
        self.execute(sql)
        self.commit()
