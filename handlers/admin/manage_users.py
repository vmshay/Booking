from bot import database
from aiogram import types, Dispatcher
from bot.functions import beauty_reg_request
from bot.keyboards import manage_kb, register_kb


async def list_users(message: types.Message):
    db = database.Database()
    if not db.sql_fetchone(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    if not db.sql_parse_users("select id,name,phone from user_table where approved = '0'"):
        await message.answer('Заявки на регистрацию отсутствуют')
    else:
        data = db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
        await message.answer(beauty_reg_request(data[0]),
                             reply_markup=manage_kb(f"u_accept:{data[0]['ID']}", f"u_deny:{data[0]['ID']}", f"u_next:0",
                                                    f"u_prev:0", f"1/{len(data)}"))


async def next_user_page(call: types.CallbackQuery):
    db = database.Database()
    data = db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.data.split(":")[1]) + 1

    if not data:
        await call.message.answer('Заявки на регистрацию отсутствуют')
    if index == len(data):
        pass
    else:
        user_id = data[index]['ID']
        await call.message.edit_text(beauty_reg_request(data[index]),
                                     reply_markup=manage_kb(f"u_accept:{user_id}", f"u_deny:{user_id}", f"u_next:{index}",
                                                            f"u_prev:{index}", f"{index + 1}/{len(data)}"))


async def prev_user_page(call: types.CallbackQuery):
    db = database.Database()
    data = db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.data.split(":")[1])-1
    if not data:
        await call.message.answer('Заявки на регистрацию отсутствуют')
    elif index < 0:
        pass
    else:
        user_id = data[index]['ID']
        await call.message.edit_text(beauty_reg_request(data[index]),
                                     reply_markup=manage_kb(f"u_accept:{user_id}", f"u_deny:{user_id}", f"u_next:{index}",
                                                            f"u_prev:{index}", f"{index + 1}/{len(data)}"))


async def accept_user(call: types.CallbackQuery):
    db = database.Database()
    data = db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.message.reply_markup.inline_keyboard[1][1].text.split("/")[0])-1

    if len(data) == 1:
        user_id = data[index]['ID']
        db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.delete()
        await call.message.answer('Заявки на регистрацию отсутствуют')
    elif index == 0:
        user_id = data[index]['ID']
        db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index+1]),
                                     reply_markup=manage_kb(f"u_accept:{user_id}", f"u_deny:{user_id}", f"u_next:{index + 1}",
                                                            f"u_prev:{index + 1}", f"{index + 1}/{len(data) - 1}"))
    elif index == len(data)-1:
        user_id = data[index]['ID']
        db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index-1]),
                                     reply_markup=manage_kb(f"u_accept:{user_id}", f"u_deny:{user_id}", f"u_next:{index - 1}",
                                                            f"u_prev:{index - 1}", f"{index}/{len(data) - 1}"))
    else:
        user_id = data[index]['ID']
        db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index-1]),
                                     reply_markup=manage_kb(f"u_accept:{user_id}", f"u_deny:{user_id}", f"u_next:{index}",
                                                            f"u_prev:{index}", f"{index}/{len(data) - 1}"))


# Регистрация команд
def admin_handlers(dp: Dispatcher):
    dp.register_message_handler(list_users, text='👤 Управление пользователями')
    dp.register_callback_query_handler(next_user_page, text_startswith='u_next')
    dp.register_callback_query_handler(prev_user_page, text_startswith='u_prev')
    dp.register_callback_query_handler(accept_user, text_startswith='u_accept')
