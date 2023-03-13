from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_kb():
    keyboard = InlineKeyboardMarkup()
#     bind = InlineKeyboardButton()
#     my_events = InlineKeyboardButton()
#     all_events = InlineKeyboardButton()
# '🎯 Запланировать мероприятие'
# '🗒 Мои события'
# '📅 Все события'
# "👮 Управление"


def register_kb():
    keyboard = InlineKeyboardMarkup()
    register = InlineKeyboardButton("Регистрация", callback_data="register")
    keyboard.add(register)
    return keyboard
