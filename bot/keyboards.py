from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.functions import month_text


# Основная
def main_kb():
    keyboard = InlineKeyboardMarkup()
    plain = InlineKeyboardButton(text='🎯 Запланировать мероприятие', callback_data='plain')
    my_events = InlineKeyboardButton(text='🗒 Мои события', callback_data='my_events')
    all_events = InlineKeyboardButton(text='📅 Все события', callback_data='all_events')
    manage = InlineKeyboardButton(text='👮 Управление', callback_data='manage')
    keyboard.add(plain)
    keyboard.add(my_events)
    keyboard.add(all_events)
    # keyboard.add(manage)
    return keyboard


def register_kb():
    keyboard = InlineKeyboardMarkup()
    register = InlineKeyboardButton("Регистрация", callback_data="register")
    keyboard.add(register)
    return keyboard


def reset_register_kb():
    keyboard = InlineKeyboardMarkup()
    reset = InlineKeyboardButton("Отменить регистрацию", callback_data="res_register")
    keyboard.add(reset)
    return keyboard


def new_user_kb(accept, deny, u_id):
    keyboard = InlineKeyboardMarkup()
    accept = InlineKeyboardButton("Одобрить", callback_data=f"{accept}:{u_id}")
    deny = InlineKeyboardButton("Отклонить", callback_data=f"{deny}:{u_id}")
    keyboard.add(accept, deny)
    return keyboard



def events_range_kb():
    keyboard = InlineKeyboardMarkup()
    today_button = InlineKeyboardButton(text="За сегодня", callback_data="today")
    week_button = InlineKeyboardButton(text="За неделю", callback_data="week")
    month_button = InlineKeyboardButton(text="За месяц", callback_data="month")
    keyboard.add(today_button, week_button, month_button)
    return keyboard


def cancel_booking():
    keyboard = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="Отменить", callback_data="cancel_booking")
    keyboard.add(cancel_button)
    return keyboard


def events_kb():
    keyboard = InlineKeyboardMarkup()
    booking_button = InlineKeyboardButton(text='Забронировать', callback_data="booking")
    back_button = InlineKeyboardButton(text='Отменить', callback_data="cancel_booking")
    keyboard.add(back_button, booking_button)
    return keyboard


# Генератор календаря
def make_calendar(month, days_in_month, m_prev, m_next):
    mont_text = InlineKeyboardButton(text=month_text(month - 1), callback_data='NULL')
    keyboard = InlineKeyboardMarkup(row_width=7)
    prev_month = InlineKeyboardButton(text="<<", callback_data=m_prev)
    next_month = InlineKeyboardButton(text=">>", callback_data=m_next)
    cancel_button = InlineKeyboardButton(text="Отменить", callback_data="cancel_booking")

    keyboard.row_width = 7
    for i in range(1, days_in_month + 1, 1):
        if i < 10:
            day = f"0{i}"
        else:
            day = i
        date_i = InlineKeyboardButton(text=str(i), callback_data=f"date_2022-{str(month)}-{str(day)}")
        keyboard.insert(date_i)

    keyboard.add(prev_month, mont_text, next_month)
    keyboard.add()
    keyboard.add(cancel_button)
    return keyboard
