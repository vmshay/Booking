import phonenumbers
import re
import datetime
from datetime import date, timedelta
from bot import database
import intervaltree


def validate_phone(number):
    number = number.replace('-', '')
    number = number.replace(' ', '')

    if len(number) == 10:
        number = "+7" + number
    elif len(number) == 11 and number[0] == '8':
        number = "+7" + number[1:]

    try:
        parse_phone = phonenumbers.parse(number)
        if phonenumbers.is_possible_number(parse_phone):
            return True
        else:
            return False
    except:
        return False


def reject_cmd(text):
    if "/" in text:
        return True
    else:
        return False


def reject_latin(text):
    if re.search(r'[a-zA-Z0-9]', text):
        return True
    else:
        return False


def validate_fio(text):
    if len(text.split(' ')) < 3:
        return True
    else:
        return False


def validate_time():
    pass


def beauty_reg_request(data):
    result = (f"ФИО: {data['ФИО']}\n"
              f"Контакт: {data['Номер телефона']}")

    return result


def beauty_booked_time(data):
    result = ""
    for elem in data:
        result += f"{elem['e_start']} - {elem['e_end']}\n"
    return result


def beauty_event_request(data):
    result = (f"ID: {data['ID']}\n"
              f"Инициатор: {data['Инициатор']}\n"
              f"Телефон: {data['Номер телефона']}\n"
              f"Описание: {data['Описание']}\n"
              f"Начало в: {data['Начало в']}\n"
              f"Конец в: {data['Конец в']}")
    return result


def beauty_all_events(data):
    result = ""
    for elem in data:
        result += f"<b>Инициатор:</b> {elem['name']}\n" \
                  f"<b>Событие:</b> {elem['description']}\n" \
                  f"<b>Дата:</b> {elem['e_date']}\n" \
                  f"<b>Время:</b> {elem['e_start']} - {elem['e_end']}\n\n"
    return result


def make_date():
    today = datetime.datetime.now()
    return datetime.datetime.strftime(today, '%d.%m.%Y')


def date_range(data):
    today = date.today()
    weekday = today.weekday()
    days_per_month = {1: 31, 2: 28, 3: 30, 4: 31, 5: 30, 6: 31,
                      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if data == "today":
        return today

    if data == "week":
        first = today - timedelta(days=weekday)
        # upper bound
        last = today + timedelta(days=(6 - weekday))
        return f"{first} and {last}"

    if data == "month":
        first = today.replace(day=1)
        try:
            last = today.replace(day=days_per_month[today.month])
        except ValueError:
            if today.month == 2:  # Not a leap year
                last = today.replace(day=28)
            else:
                raise
        return f"{first} and {last}"


def to_quotes(data):
    data = "'" + str(data) + "'"
    return data


def time_validator(data):
    re_pattern = "^(2[0-3]|[01]?[0-9])(:|\.)([0-5]?[0-9])( |-)(2[0-3]|[01]?[0-9])(:|\.)([0-5]?[0-9])$"
    if re.match(re_pattern, data):
        if len(data.split(" ")) == 2:
            return True
        elif len(data.split("-")) == 2:
            return True
        else:
            return False
    else:
        return False


def normalize_time(data):
    if len(data.split(" ")) == 2:
        if len(data.split(" ")[0]) == 4:
            data = "0" + data
            return data.replace(".", ":").split(" ")
        else:
            return data.replace(".", ":").split(" ")
    elif len(data.split("-")) == 2:
        if len(data.split("-")[0]) == 4:
            data = "0" + data
            return data.replace(".", ":").split("-")
        else:
            return data.replace(".", ":").split("-")
    else:
        return False


def check_overlap(start, end, date):
    it = intervaltree.IntervalTree()
    db = database.Database()
    times = db.sql_fetchall(f"select e_start,e_end from events_table where e_date = {date}")
    for time in times:
        it.addi(time['e_start'], time['e_end'])
        return not it.overlaps(start, end)


def parse_events(data):
    events_list = []
    for elem in data:
        event = {"ID": elem['id'],
                 "Инициатор": elem['name'],
                 "Номер телефона": elem['phone'],
                 "Описание": elem['description'],
                 "Начало в": elem['e_start'],
                 "Конец в": elem['e_end']}

        events_list.append(event)
    return events_list

