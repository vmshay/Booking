import database
from aiogram import types, Dispatcher
from functions import beauty_reg_request
from keyboards import user_manage_kb


async def list_users(message: types.Message):
    Db = database.Database()
    if not Db.sql_parse_users("select id,name,phone from user_table where approved = '0'"):
        await message.answer('Заявки на регистрацию отсутствуют')
    else:
        data = Db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
        await message.answer(beauty_reg_request(data[0]),
                             reply_markup=user_manage_kb(f"accept:{data[0]['ID']}",
                                                         f"deny:{data[0]['ID']}",
                                                         f"next:0",
                                                         f"prev:0",
                                                         f"1/{len(data)}"))


async def next_user_page(call: types.CallbackQuery):
    Db = database.Database()
    data = Db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.data.split(":")[1]) + 1

    if not data:
        await call.message.answer('Заявки на регистрацию отсутствуют')
    if index == len(data):
        pass
    else:
        # print(f"next: {index}")
        user_id = data[index]['ID']
        await call.message.edit_text(beauty_reg_request(data[index]),
                                     reply_markup=user_manage_kb(f"accept:{user_id}",
                                                                 f"deny:{user_id}",
                                                                 f"next:{index}",
                                                                 f"prev:{index}",
                                                                 f"{index + 1}/{len(data)}"))


async def prev_user_page(call: types.CallbackQuery):
    Db = database.Database()
    data = Db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.data.split(":")[1])-1
    # print(f"prev_index{index}")
    if not data:
        await call.message.answer('Заявки на регистрацию отсутствуют')
    elif index < 0:
        pass
    else:
        user_id = data[index]['ID']
        await call.message.edit_text(beauty_reg_request(data[index]),
                                     reply_markup=user_manage_kb(f"accept:{user_id}",
                                                                 f"deny:{user_id}",
                                                                 f"next:{index}",
                                                                 f"prev:{index}",
                                                                 f"{index+1}/{len(data)}"))


async def accept_user(call: types.CallbackQuery):
    Db = database.Database()
    data = Db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    # data = Db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
    index = int(call.message.reply_markup.inline_keyboard[1][1].text.split("/")[0])-1
    # print(index)


    if len(data) == 1:
        user_id = data[index]['ID']
        Db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.delete()
        await call.message.answer('Заявки на регистрацию отсутствуют')
    elif index == 0:
        user_id = data[index]['ID']
        Db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index+1]),
                                     reply_markup=user_manage_kb(f"accept:{user_id}",
                                                                 f"deny:{user_id}",
                                                                 f"next:{index + 1}",
                                                                 f"prev:{index + 1}",
                                                                 f"{index+1}/{len(data) - 1}"))
    elif index == len(data)-1:
        user_id = data[index]['ID']
        Db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index-1]),
                                     reply_markup=user_manage_kb(f"accept:{user_id}",
                                                                 f"deny:{user_id}",
                                                                 f"next:{index - 1}",
                                                                 f"prev:{index - 1}",
                                                                 f"{index}/{len(data) - 1}"))
    else:
        user_id = data[index]['ID']
        Db.sql_query_send(f"UPDATE booking.user_table SET approved='1' WHERE id={user_id}")
        await call.message.edit_text(beauty_reg_request(data[index-1]),
                                     reply_markup=user_manage_kb(f"accept:{user_id}",
                                                                 f"deny:{user_id}",
                                                                 f"next:{index}",
                                                                 f"prev:{index - 1}",
                                                                 f"{index}/{len(data) - 1}"))


async def events_manage(message: types.message):
    await message.answer(f"Управление мероприятиями\n"
                         f"Здесь вы можете управлять заявками мероприятий\n\n")


# Регистрация команд
def admin_handlers(dp: Dispatcher):
    dp.register_message_handler(list_users, text='👤 Управление пользователями')
    dp.register_message_handler(events_manage, text='🎫 Управление мероприятиями')

    dp.register_callback_query_handler(next_user_page, text_startswith='next')
    dp.register_callback_query_handler(prev_user_page, text_startswith='prev')
    dp.register_callback_query_handler(accept_user, text_startswith='accept')
