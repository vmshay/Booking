from aiogram import types, Dispatcher
from bot.database import Database


async def all_events(call: types.CallbackQuery):
    db = Database()
    data = db.sql_fetchall('select * from user_table')
    print(data)
    db.close()
    await call.message.answer("Все события")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(all_events, text_startswith='all_events')
