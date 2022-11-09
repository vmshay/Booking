from aiogram import types, Dispatcher
from bot import database, sql
from bot.functions import beauty_all_events


async def my_events(call: types.CallbackQuery):
    db = database.Database()
    data = db.sql_fetchall(sql=sql.get_user_event(call.from_user.id))
    if len(data) == 0:
        await call.message.answer("Вы не планировали мероприятия")
    else:
        await call.message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))


def register(dp: Dispatcher):
    dp.register_callback_query_handler(my_events, text='my_events')
