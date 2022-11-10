from datetime import datetime

from bot.dispatcher import bot
import bot.config as cnf
from bot.keyboards import new_user_kb


async def new_bug(data):
    msg = f"<b>Обратная связь</b>\n" \
          f"Сообщение: {data['bug']}\n" \
          f"Отправитель: @{data['from_user']}\n"
    await bot.send_message(cnf.CHAT_ID, msg)


async def new_user(data):
    msg = f"<b>Новый пользователь</b>\n" \
          f"TG: @{data['tg']}\n" \
          f"ФИО: {data['FIO']}\n" \
          f"Номер телефона: {data['number']}"
    await bot.send_message(cnf.CHAT_ID, msg, reply_markup=new_user_kb(f"u_accept", f"u_deny", data['id']))


async def new_event(data):
    msg = f"<b>Новая заявка мероприятия</b>\n\n" \
          f"Дата: {data['date']}\n" \
          f"ФИО: {data['username']}\n" \
          f"C {data['t_start']} до {data['t_end']}\n" \
          f"Описание {data['description']}"
    await bot.send_message(cnf.CHAT_ID, msg, reply_markup=new_user_kb(f"e_accept", f"e_deny", data['id']))


async def notify_user_reg_accept(u_id):
    msg = f"Учетная запись подтверждена"
    await bot.send_message(u_id, msg)


async def notify_user_reg_deny(u_id):
    msg = f"Учетная запись отклонена"
    await bot.send_message(u_id, msg)


async def notify_user_event_accept(u_id):
    msg = f"Заявка мероприятия одобрена"
    await bot.send_message(u_id, msg)


async def notify_user_event_deny(u_id):
    msg = f"Заявка мероприятия отклонена"
    await bot.send_message(u_id, msg)


async def trash_msg(msg, user):
    msg = f"User: @{user}\n" \
          f"Msg: {msg}"
    await bot.send_message(cnf.TRASH_CHAT, msg)
