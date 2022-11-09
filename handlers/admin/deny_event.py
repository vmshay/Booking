from aiogram import types, Dispatcher
from bot import database
from bot.notifications import notify_user_event_deny


async def deny_event(call: types.CallbackQuery):
    db = database.Database()
    t_id = call.data.split(":")[1]
    client_id = db.sql_fetchone(f"select owner from events_table where id = {t_id}")
    db.sql_query_send(f"delete from events_table where id = {t_id}")
    db.sql_query_send(f"ALTER TABLE events_table  AUTO_INCREMENT={int(t_id)-1};")
    await call.message.edit_text("Мероприятие отклонено")
    await notify_user_event_deny(client_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(deny_event, text_startswith='e_deny:')
