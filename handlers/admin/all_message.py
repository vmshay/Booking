from aiogram import types, Dispatcher
from bot.notifications import trash_msg


async def handle_all(message: types.Message):
    await trash_msg(message.text,message.from_user.username)


def register(dp: Dispatcher):
    dp.register_message_handler(handle_all, chat_type='private')