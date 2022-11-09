import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from bot import database
from bot.states import RegisterStates
from bot.keyboards import reset_register_kb, register_kb
from bot.functions import validate_phone, reject_latin, reject_cmd, validate_fio
from bot.notifications import new_user


async def registration(call: types.CallbackQuery):
    await call.message.edit_text(f"Введите номер телефона\n"
                                 f"Возможные форматы:\n\n"
                                 f"<b>+79995554433</b>\n"
                                 f"<b>9997771122</b>\n"
                                 f"<b>89995554433</b>\n"
                                 f"<b>8-999-888-11-22</b>\n"
                                 f"<b>+7-999-888-11-22</b>", reply_markup=reset_register_kb())
    await RegisterStates.phone.set()


async def get_number(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await state.update_data(number=message.text)
        await message.delete()
        msg = await message.answer(f"Укажите ФИО\n"
                                   f"Например: Иванов Иван Иванович")

        await RegisterStates.FIO.set()
        await asyncio.sleep(60)
        await msg.delete()
    else:
        await message.delete()
        msg = await message.answer(f"Указан некорректный номер телефона")
        await asyncio.sleep(5)
        await msg.delete()


async def get_fio(message: types.Message, state: FSMContext):
    db = database.Database()
    if reject_cmd(message.text):
        await message.delete()
        msg = await message.answer("Нельзя использовать команды")
        await asyncio.sleep(5)
        await msg.delete()
    elif reject_latin(message.text):
        await message.delete()
        msg = await message.answer("Нельзя использовать латиницу и символы")
        await asyncio.sleep(5)
        await msg.delete()
    elif validate_fio(message.text):
        await message.delete()
        msg = await message.answer("Необходимо указать полное ФИО")
        await asyncio.sleep(5)
        await msg.delete()
    else:
        await message.delete()

        await state.update_data(FIO=message.text)
        await state.update_data(id=message.from_user.id)
        await state.update_data(tg=message.from_user.username)
        reg_data = await state.get_data()
        await state.finish()
        msg = await message.answer(f"Заявка отправлена")
        db.sql_query_send(f"INSERT INTO user_table (tg_id,name,phone)"
                          f"VALUES ({reg_data['id']},"
                          f"'{reg_data['FIO']}',"
                          f"'{reg_data['number']}')")
        await new_user(reg_data)
        await asyncio.sleep(5)
        await msg.delete()


async def reset_register(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"🤖Вас приветствует бот 405 кабинета🤖\n"
                                 f"\n"
                                 f"Для доступа к функционалу необходимо зарегистрироваться\n"
                                 f"", reply_markup=register_kb())


def register(dp: Dispatcher):
    dp.register_callback_query_handler(registration, text="register")
    dp.register_callback_query_handler(reset_register, text="res_register", state=[RegisterStates.phone,
                                                                                   RegisterStates.FIO])
    dp.register_message_handler(get_number, state=RegisterStates.phone)
    dp.register_message_handler(get_fio, state=RegisterStates.FIO)

