from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import calendar
import datetime


# Основная
button_bind = KeyboardButton('🎯 Запланировать мероприятие')
button_my = KeyboardButton('🗒 Мои события')
button_all = KeyboardButton('📅 Все события')
button_config = KeyboardButton("👮 Управление")
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)

main_kb.add(button_bind, button_config)
main_kb.add(button_my, button_all)

# регистрация
register_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_register = KeyboardButton('Зарегистрироваться')
register_kb.add(button_register)

# отмена регистрации
reset_register_kb = ReplyKeyboardMarkup(resize_keyboard=True)
res_button = KeyboardButton("Отменить регистрацию")
reset_register_kb.add(res_button)

# Проверка статуса регистрации
check_register_kb = ReplyKeyboardMarkup(resize_keyboard=True)
check_button = KeyboardButton("Проверить статус заявки")
check_register_kb.add(check_button)


# Для администраторов
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
waiting_users = KeyboardButton("👤 Управление пользователями")
waiting_events = KeyboardButton("🎫 Управление мероприятиями")
back = KeyboardButton("Выйти")
admin_keyboard.add(waiting_events, waiting_users)
admin_keyboard.add(back)


# Клавиатура для заявок
def user_manage_kb(b_accept, b_deny, b_next, b_prev, b_count):
    keyboard = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton(text="Одобрить", callback_data=b_accept)
    deny_button = InlineKeyboardButton(text="Отклонить", callback_data=b_deny)
    count_button = InlineKeyboardButton(text=b_count, callback_data="NULL")  # f"{index}/{len(data)}"
    next_button = InlineKeyboardButton(text="Далее", callback_data=b_next)   # f"next:0"
    prev_button = InlineKeyboardButton(text="Назад", callback_data=b_prev)

    keyboard.add(accept_button, deny_button)
    keyboard.add(prev_button, count_button, next_button)
    return keyboard


def events_range_kb():
    keyboard = InlineKeyboardMarkup()
    today_button = InlineKeyboardButton(text="За сегодня",callback_data="today")
    week_button = InlineKeyboardButton(text="За неделю", callback_data="week")
    month_button = InlineKeyboardButton(text="За месяц", callback_data="month")
    keyboard.add(today_button,week_button,month_button)
    return keyboard

# Генератор календаря
def make_calendar():
    current_date = datetime.date.today()
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    month = datetime.datetime.today().month
    keyboard = InlineKeyboardMarkup(row_width=7)
    button_today = InlineKeyboardButton(text="Сегодня", callback_data="today")
    button_tomorrow = InlineKeyboardButton(text="Завтра", callback_data="tomorrow")
    button_after_tomorrow = InlineKeyboardButton(text="Послезавтра", callback_data="after_tomorrow")

    for i in range(1, days_in_month+1, 1):
        date_i = InlineKeyboardButton(text=str(i), callback_data=f"date_2022-{str(month)}-{str(i)}")
        keyboard.insert(date_i)
    keyboard.add(button_today, button_tomorrow, button_after_tomorrow)
    return keyboard
