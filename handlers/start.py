import asyncio
from aiogram import types, Dispatcher
from bot.keyboards import main_kb, register_kb,   check_register_kb
from bot import database
from bot import sql
from aiogram.dispatcher.storage import FSMContext
from handlers.user.states import SendBugState, MessageToAll
from handlers.admin.notifications import new_bug, message_to_all


# @dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    db = database.Database()
    await message.delete()
    if not db.sql_fetchone(sql.check_id(message.from_user.id)):
        await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n\n"
                             "Для доступа к функциям нужно пройти простую регистрацию\n", reply_markup=register_kb)
    elif db.sql_fetchone(sql.check_approved(message.from_user.id)) == "0":
        await message.answer(f"Ваша заявка находится на рассмотрении", reply_markup=check_register_kb)
    else:
        msg = await message.answer(f"🤖Вас приветствует лакей ТТИТ🤖\n"
                                   f"\n"
                                   f"Я помогу Вам запланировать мероприятие в 405 аудитории.\n\n"
                                   f"Меня еще разрабатыают по этому умею немного.\n\n"
                                   f"Вот мои функции:\n"
                                   f"Запланировать мероприятие\n"
                                   f"Мои события\n"
                                   f"Все события\n\n"
                                   f"Если есть пожелания или замечания\n"
                                   f"Можете обратиться к @FeldwebelWillman\n"
                                   f"Или воспользовтаься обратной связью /feedback",
                                   reply_markup=main_kb)
        await asyncio.sleep(10)
        await msg.delete()


async def stop_cmd(message: types.Message):
    if message.from_user.id == 338836490:
        await message.answer("Остановка")
    else:
        await message.answer("Я слушаюсь только создателя")


async def send_report(message: types.Message):
    await message.delete()
    await SendBugState.send_bug.set()
    msg = await message.answer("Опишите проблему")
    await asyncio.sleep(5)
    await msg.delete()


async def get_report(message: types.Message, state: FSMContext):
    await state.update_data(bug=message.text)
    await state.update_data(from_user=message.from_user.username)
    data = await state.get_data()
    await state.finish()
    await new_bug(data)
    await message.delete()


async def broadcast_cmd(message: types.Message):
    await message.delete()
    await MessageToAll.send_message.set()
    msg = await message.answer("Введите сооьщение которое будет отправленно всем пользователям")
    await asyncio.sleep(5)
    await msg.delete()


async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(bug=message.text)
    await state.update_data(from_user=message.from_user.username)
    data = await state.get_data()
    await state.finish()
    await message_to_all(data)
    await message.delete()


async def delete_all_msg(message: types.Message):
    await asyncio.sleep(5)
    await message.delete()


def main_register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start', 'help'])
    dp.register_message_handler(stop_cmd, commands=['stop'])
    dp.register_message_handler(send_report, commands=['feedback'])
    dp.register_message_handler(get_report, state=SendBugState.send_bug)
    dp.register_message_handler(broadcast_cmd, commands=['broadcast'])
    dp.register_message_handler(get_message, state=MessageToAll.send_message)
    dp.register_message_handler(delete_all_msg)

