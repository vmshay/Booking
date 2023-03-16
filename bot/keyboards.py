from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_kb():
    keyboard = InlineKeyboardMarkup()
    bind = InlineKeyboardButton('🎯 Запланировать мероприятие', callback_data='bind_event')
    my_events = InlineKeyboardButton('🗒 Мои события', callback_data='my_events')
    all_events = InlineKeyboardButton('📅 Все события', callback_data='all_events')
    keyboard.add(bind)
    keyboard.add(my_events)
    keyboard.add(all_events)
    return keyboard


def register_kb():
    keyboard = InlineKeyboardMarkup()
    register = InlineKeyboardButton("Регистрация", callback_data="register")
    keyboard.add(register)
    return keyboard


def events_range_kb():
    keyboard = InlineKeyboardMarkup()
    today_button = InlineKeyboardButton(text="За сегодня", callback_data="today")
    week_button = InlineKeyboardButton(text="За неделю", callback_data="week")
    month_button = InlineKeyboardButton(text="За месяц", callback_data="month")
    keyboard.add(today_button, week_button, month_button)
    return keyboard
