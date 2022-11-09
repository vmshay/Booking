from aiogram import types, Dispatcher
from bot import database
from bot.notifications import notify_user_reg_accept


async def accept_user(call: types.CallbackQuery):
    # print(call.data)
    u_id = call.data.split(":")[1]

    db = database.Database()
    username = db.sql_fetchone(f"select name from user_table where tg_id = {call.from_user.id}")
    await call.message.edit_text(f"{username} подтвердил учетную запись\n"
                                 f"")
    db.sql_query_send(f"update user_table set approved ='1' where tg_id = {u_id}")
    await notify_user_reg_accept(u_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(accept_user, text_startswith='u_accept:')