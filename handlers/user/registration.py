from aiogram import types, Dispatcher
from handlers.user.states import RegisterStates
from bot.functions import validate_fio, validate_phone, reject_latin, reject_cmd
from aiogram.dispatcher.storage import FSMContext
from bot.keyboards import reset_register_kb, register_kb, main_kb, check_register_kb
from bot import database, sql
from handlers.admin.notifications import new_user

async def registration(message: types.Message):
    db = database.Database()
    await message.delete()
    if db.sql_fetchone(f'select tg_id from user_table where tg_id = {message.from_user.id} and approved = 0'):
        await message.answer("Ваша заявка находится на рассмотрернии", reply_markup=check_register_kb)
    elif db.sql_fetchone(f'select tg_id from user_table where tg_id = {message.from_user.id} and approved = 1'):
        msg = await message.answer("Вы зарегистрированны", reply_markup=main_kb)
        await msg.delete()
    else:
        await message.answer(f"Дkя регистрации необходимо будет указать\n"
                             f"Номер телефона и "
                             f"Фамилию Имя Отчество")

        await message.answer(f"Введите номер телефона\n"
                             f"Возможные форматы:\n\n"
                             f"<b>+79995554433</b>\n"
                             f"<b>9997771122</b>\n"
                             f"<b>89995554433</b>\n"
                             f"<b>8-999-888-11-22</b>\n"
                             f"<b>+7-999-888-11-22</b>", reply_markup=reset_register_kb)
        await RegisterStates.phone.set()


async def check_reg_status(message: types.Message):
    db = database.Database()
    await message.delete()
    if db.sql_fetchone(f'select tg_id from user_table where tg_id = {message.from_user.id} and approved = 0'):
        await message.answer("Ваша заявка находится на рассмотрернии", reply_markup=check_register_kb)
    elif db.sql_fetchone(f'select tg_id from user_table where tg_id = {message.from_user.id} and approved = 1'):
        await message.answer("Вы зарегистрированны", reply_markup=main_kb)
    else:
        await message.answer("Вы не зарегистрированны", reply_markup=register_kb)


async def get_number(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await state.update_data(number=message.text)
        await message.answer(f"Теперь укажите ФИО\n"
                             f"Например: Иванов Иван Иванович", reply_markup=reset_register_kb)
        await RegisterStates.FIO.set()
    else:
        await message.delete()
        await message.answer(f"Указан некорректный номер телефона", reply_markup=reset_register_kb)


async def get_fio(message: types.Message, state: FSMContext):
    db = database.Database()
    if reject_cmd(message.text):
        await message.delete()
        await message.answer("Нельзя использовать команды", reply_markup=reset_register_kb)
    elif reject_latin(message.text):
        await message.delete()
        await message.answer("Нельзя использовать латиницу и символы", reply_markup=reset_register_kb)
    elif validate_fio(message.text):
        await message.answer("Необходимо указать полное ФИО", reply_markup=reset_register_kb)
    else:
        await state.update_data(FIO=message.text)
        await state.update_data(id=message.from_user.id)
        reg_data = await state.get_data()
        await message.answer(f"Спасибо за регистрацию\n"
                             f"Вы сможете воспользоваться функциями после одобрения\n", reply_markup=check_register_kb)

        db.sql_query_send(sql.sql_send(reg_data))
        await state.finish()
        await new_user()


async def reset_register(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Регистрация отменена", reply_markup=register_kb)


def register_handlers(dp: Dispatcher):
    # хендлеры регистрации
    dp.register_message_handler(registration, text="Зарегистрироваться")
    dp.register_message_handler(check_reg_status, text="Проверить статус заявки")
    dp.register_message_handler(reset_register, text='Отменить регистрацию', state=[RegisterStates.phone,
                                                                                    RegisterStates.FIO])
    dp.register_message_handler(get_number, state=RegisterStates.phone)
    dp.register_message_handler(get_fio, state=RegisterStates.FIO)
