from mysql.connector import connect
import config as conf


def sql_check_user(db_query):
    conn = connect(host=conf.DB_HOST,
                   user=conf.DB_USER,
                   password=conf.DB_PASS,
                   database=conf.DB_NAME)

    cursor = conn.cursor()
    cursor.execute(db_query)
    result_set = cursor.fetchall()
    if len(result_set) == 0:
        return False
    elif len(result_set) > 0:
        return True


def sql_simple_check(db_query, field):
    conn = connect(host=conf.DB_HOST,
                   user=conf.DB_USER,
                   password=conf.DB_PASS,
                   database=conf.DB_NAME)

    cursor = conn.cursor(dictionary=True)
    cursor.execute(db_query)
    result_set = cursor.fetchone()
    if result_set[field] == '0':
        return False
    else:
        return True


def sql_parse_users(db_query):
    conn = connect(host=conf.DB_HOST,
                   user=conf.DB_USER,
                   password=conf.DB_PASS,
                   database=conf.DB_NAME)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(db_query)
    result_set = cursor.fetchall()
    # print(len(result_set))
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


def sql_query_send(db_query):
    conn = connect(host=conf.DB_HOST,
                   user=conf.DB_USER,
                   password=conf.DB_PASS,
                   database=conf.DB_NAME)

    cursor = conn.cursor()
    cursor.execute(db_query)
    conn.commit()
    conn.close()


# sql_query_users(f"select name,phone from user_table where approved = '0'")
# print(sql_simple_check(f"select approved from user_table where tg_id='338836490'"))
# print(sql_parse_users(f"select id, name,phone from user_table where approved = '0'"))
# print(sql_simple_check(f"select admin from user_table where tg_id = '338836490'", "admin"))
# print(not not sql_query_single_get(f"select tg_id from user_table where tg_id = '11'"))
# sql_query(f"INSERT INTO user_table (tg_id,name,phone) VALUES ('123123','ФФ ыв ывыв','89539299323')")
# select name,phone from user_table where approved = '0'
