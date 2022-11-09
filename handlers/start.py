import asyncio
from aiogram import types, Dispatcher
from bot.keyboards import main_kb, register_kb
from bot import database
from bot import sql
from aiogram.dispatcher.storage import FSMContext
from bot.states import SendBugState, MessageToAll
from bot.notifications import new_bug


# @dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    db = database.Database()
    if message.chat.type == 'private':
        if not db.sql_fetchone(sql.check_id(message.from_user.id)):
            await message.answer(f"🤖Вас приветствует бот 405 кабинета🤖\n"
                                 f"\n"
                                 f"Для доступа к функционалу необходимо зарегистрироваться\n"
                                 f"", reply_markup=register_kb())
        elif db.sql_fetchone(f'select approved from user_table where tg_id ={message.from_user.id}') == '0':
            msg = await message.answer("Аккаунт еще не подтвержден")
            await asyncio.sleep(5)
            await msg.delete()
        else:

            await message.answer(f"🤖Вас приветствует бот 405 кабинета🤖\n"
                                   f"Я помогу Вам запланировать мероприятие.\n\n"
                                   f"Вот что можно сделать:\n"
                                   f"<b>Запланировать мероприятие</b>\n"
                                   f"Планирование мероприятия\n\n"
                                   f"<b>Мои события</b>\n"
                                   f"События запланированные Вами\n\n"
                                   f"<b>Все события</b>\n"
                                   f"События всех пользователей\n"
                                   f"с выборкой по интервалам\n\n"
                                   f"Если есть пожелания или замечания\n"
                                   f"Можете обратиться к @FeldwebelWillman\n"
                                   f"Или воспользовтаься обратной связью /feedback",
                                   reply_markup=main_kb())
    # else:
    #     await message.answer(f"Если Вы хотите , запланировать мероприятие в 405"
    #                          f"напишите лично @TTITTechSuppBot")


async def stop_cmd(message: types.Message):
    if message.from_user.id == 338836490:
        await message.answer("Остановка")
    else:
        await message.answer("Я слушаюсь только создателя")


async def send_report(message: types.Message):
    await message.delete()
    await SendBugState.send_bug.set()
    msg = await message.answer("Опишите проблему")
    await asyncio.sleep(60)
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


def main_register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start', 'help'])
    dp.register_message_handler(stop_cmd, commands=['stop'])
    dp.register_message_handler(send_report, commands=['feedback'])
    dp.register_message_handler(get_report, state=SendBugState.send_bug)
    dp.register_message_handler(broadcast_cmd, commands=['broadcast'])
    dp.register_message_handler(get_message, state=MessageToAll.send_message)

