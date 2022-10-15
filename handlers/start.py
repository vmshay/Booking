import asyncio

import aiogram
from aiogram import types, Dispatcher
from bot.keyboards import main_kb, register_kb,   check_register_kb
from bot import database
from bot import sql


# @dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    db = database.Database()
    await message.delete()
    if not db.sql_fetchone(sql.check_id(message.from_user.id)):
        await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n\n"
                             "Для доступа к функциям нужно пройти простую регистрацию\n", reply_markup=register_kb)
    elif not db.sql_fetchone(sql.check_approved(message.from_user.id)):
        await message.answer(f"Ваша заявка находится на рассмотрернии", reply_markup=check_register_kb)
    else:
        await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n"
                             f"\n"
                             f"Я помогу Вам запланировать мероприятие в 405 аудитории.\n\n"
                             f"Меня еще разрабатыают по этому умею немного.\n\n"
                             f"Вот мои функции:\n"
                             f"Запланировать мероприятие\n"
                             f"Мои события\n"
                             f"Все события\n\n"
                             f"Если есть пожелания или замечания\n"
                             f"Можете обратиться к @FeldwebelWillman",
                             reply_markup=main_kb)


async def stop_cmd(message: types.Message):
    if message.from_user.id == 338836490:
        await message.answer("Остановка")
    else:
        await message.answer("Я слушаюсь только создателя")


def main_register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start', 'help'])
    dp.register_message_handler(stop_cmd, commands=['stop'])
