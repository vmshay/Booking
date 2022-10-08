from aiogram import types, Dispatcher
from bot.keyboards import main_kb, register_kb,   check_register_kb
from bot import database


# @dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    Db = database.Database()
    await message.delete()
    if not Db.sql_simple_check(f"select tg_id from user_table where tg_id ={message.from_user.id}"):
        await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n\n"
                             "Для доступа к функциям нужно пройти простую регистрацию\n",
                             reply_markup=register_kb)
    elif not Db.sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.answer(f"Ваша заявка находится на рассмотрернии", reply_markup=check_register_kb)
    else:
        await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n"
                             "\n"
                             "Я помогу Вам запланировать мероприятие в 405 аудитории.\n\n"
                             "Меня еще разрабатыают по этому умею немного.\n\n"
                             "Вот мои функции:\n"
                             "Запланировать мероприятие\n"
                             "Мои события\n"
                             "Все события(В разработке)\n\n"
                             "Если есть пожелания или замечания\n"
                             "Можете обратиться к создателю @FeldwebelWillman",
                             reply_markup=main_kb)


def main_register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start', 'help'])
