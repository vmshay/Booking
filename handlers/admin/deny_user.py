from aiogram import types, Dispatcher
from bot import database
from bot.notifications import notify_user_reg_deny


async def deny_user(call: types.CallbackQuery):
    u_id = call.data.split(":")[1]
    db = database.Database()
    username = db.sql_fetchone(f"select name from user_table where tg_id = {call.from_user.id}")
    # db.sql_query_send(f"update")
    await call.message.edit_text(f"{username} отклонил учетную запись\n"
                                 f"")
    await notify_user_reg_deny(u_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(deny_user, text_startswith='u_deny:')
