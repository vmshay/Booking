import phonenumbers
import re
import datetime


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


def make_date():
    today = datetime.datetime.now()
    return datetime.datetime.strftime(today, '%d.%m.%Y')

