# TODO: Рассылка для администраторов
from bot.dispatcher import bot
import bot.config as cnf


async def new_event():
    await bot.send_message(cnf.CHAT_ID, "Новая заявка мероприятия")


async def new_user():
    await bot.send_message(cnf.CHAT_ID, "Новая заявка на регистрацию")


async def new_bug(data):
    msg = f"<b>Обратная связь</b>\n" \
          f"Сообщение: {data['bug']}\n" \
          f"Отправитель: {data['from_user']}\n"
    await bot.send_message(cnf.CHAT_ID, msg)


async def message_to_all(msg):
    await bot.send_message(msg)
