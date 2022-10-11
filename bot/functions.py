import phonenumbers
import re
import datetime
from datetime import date, timedelta


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


def beauty_all_events(data):
    result = (f"******************\n"
              f"Инициатор:\n{data['Инициатор']}\n\n"
              f"Событие:\n{data['Описание']}\n\n"
              f"Дата:\n{data['Дата']}\n\n"
              )
    return result


def make_date():
    today = datetime.datetime.now()
    return datetime.datetime.strftime(today, '%d.%m.%Y')


def date_range(range):
    today = date.today()
    weekday = today.weekday()
    days_per_month = {1: 31, 2: 28, 3: 30, 4: 31, 5: 30, 6: 31,
                      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if range == "today":
        return today

    if range == "week":
        first = today - timedelta(days=weekday)
        # upper bound
        last = today + timedelta(days=(6 - weekday))
        return f"{first} and {last}"

    if range == "month":
        first = today.replace(day=1)
        # вторая дата
        try:
            last = today.replace(day=days_per_month[today.month])
        except ValueError:
            if today.month == 2:  # Not a leap year
                last = today.replace(day=28)
            else:
                raise
        return f"{first} and {last}"


def get_all_events(data):
    pass



    #
    # def sql_parse_user_events(self, sql: str):
    #     self.execute(sql)
    #     result_set = self.fetchall()
    #     events_list = []
    #     if len(result_set) == 0:
    #         return False
    #     elif len(result_set) > 0:
    #         for row in result_set:
    #             event_data = f"Описание {row['description']}\n Дата {row['dat']}"
    #             events_list.append(event_data)
    #         return events_list
