import mysql.connector
import config as conf


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(host=conf.DB_HOST,
                                                  user=conf.DB_USER,
                                                  password=conf.DB_PASS,
                                                  database=conf.DB_NAME)
        self.cursor = self.connection.cursor(dictionary=True)

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

    def sql_simple_check(self, sql: str):
        self.execute(sql)
        response = self.fetchone()
        if response is None:
            return False
        else:
            for v in response.values():
                return v

    def sql_parse_users(self, sql: str):
        self.execute(sql)
        result_set = self.fetchall()
        users_list = []
        if len(result_set) == 0:
            return False
        elif len(result_set) > 0:
            for row in result_set:
                users_data = {"ID": row['id'],
                              "ФИО": row['name'],
                              "Номер телефона": row['phone']}
                users_list.append(users_data)
            return users_list

    def sql_query_send(self, sql):
        self.execute(sql)
        self.commit()
        self.close()


# Db = Database()
# data = Db.sql_simple_check("select tg_id from user_table where tg_id = 338836490 and approved = 0")
# print(data)

