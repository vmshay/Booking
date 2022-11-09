from aiogram import types, Dispatcher
from bot import database
from bot.notifications import notify_user_event_accept


async def accept_event(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    client_id = db.sql_fetchone(f"select owner from events_table where id = {t_id}")
    db.sql_query_send(f"update events_table set approved = '1' where id = {t_id}")
    await call.message.edit_text("Заявка одобрена")
    await notify_user_event_accept(client_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_event, text_startswith='e_accept:')
