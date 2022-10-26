

def check_admin(data):
    sql = f"select admin from user_table where tg_id = {data}"
    return sql


def check_id(data):
    sql = f'select tg_id from user_table where tg_id ={data}'
    return sql


def check_approved(data):
    sql = f'select approved from user_table where tg_id ={data}'
    return sql


def get_user_event(data):
    sql = f"select events_table.description, user_table.name, events_table.e_date, events_table.e_start, events_table.e_end" \
        f" from events_table" \
        f" inner join user_table on events_table.owner = user_table.tg_id where events_table.owner={data}"
    return sql


def get_all_events(data):
    sql = f"select events_table.description, user_table.name, events_table.e_date, events_table.e_start, events_table.e_end from events_table" \
          f" inner join user_table on events_table.owner = user_table.tg_id where events_table.e_date={data}"

    return sql


def get_range_events(data):
    sql = f"select events_table.description, user_table.name, events_table.e_date, events_table.e_start, events_table.e_end " \
                                   f"from events_table inner join user_table " \
                                   f"on events_table.owner = user_table.tg_id " \
                                   f"where events_table.e_date between {data}"
    return sql


def sql_send(data):
    sql = f"INSERT INTO user_table (tg_id,name,phone) VALUES ({data['id']},'{data['FIO']}',{data['number']})"
    return sql


def sql_booked(data):
    sql = f"select events_table.id, user_table.name, user_table.phone, events_table.description, events_table.e_start, events_table.e_end from events_table inner join user_table on events_table.owner = user_table.tg_id WHERE events_table.e_date = '{data}'"
    return sql


def sql_booked_time(data):
    sql = f"select e_start ,e_end from events_table where e_date = '{data}'"
    return sql


def sql_send_event(data):
    sql = f"insert into events_table (e_date, owner, description, e_start, e_end) values ({data['date']},{data['owner']},'{data['description']}','{data['t_start']}','{data['t_end']}')"
    return sql


def sql_manage_events():
    sql = f"select user_table.tg_id, events_table.id, user_table.name, user_table.phone, events_table.description, events_table.e_date, events_table.e_start, events_table.e_end from events_table inner join user_table on events_table.owner = user_table.tg_id WHERE events_table.approved = 0"
    return sql


def sql_all_events():
    sql = f"select events_table.id, events_table.description, user_table.name, events_table.e_date, events_table.e_start, events_table.e_end" \
          f" from events_table" \
          f" inner join user_table on events_table.owner = user_table.tg_id where events_table.approved = '1'"
    return sql
