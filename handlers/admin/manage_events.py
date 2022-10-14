# TODO: Добавить управление мероприятиями
from aiogram import types, Dispatcher
from bot import database
from bot.functions import beauty_reg_request
from bot.keyboards import register_kb,user_manage_kb


async def list_events(message: types.Message):
    db = database.Database()
    if not db.sql_fetchone(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    if not db.sql_parse_users("select id,name,phone from user_table where approved = '0'"):
        await message.answer('Заявки на мероприятия остутствуют')
    else:
        await message.answer("заявки есть")
        # data = db.sql_parse_users("select id,name,phone from user_table where approved = '0'")
        # await message.answer("test",
        #                      reply_markup=user_manage_kb(f"accept:{data[0]['ID']}",
        #                                                  f"deny:{data[0]['ID']}",
        #                                                  f"next:0",
        #                                                  f"prev:0",
        #                                                  f"1/{len(data)}"))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(list_events, text='🎫 Управление мероприятиями')


