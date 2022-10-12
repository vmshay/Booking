from aiogram import types, Dispatcher
from bot.keyboards import register_kb, main_kb, admin_keyboard
from bot import database


async def enter_admin_menu(message: types.message):
    db = database.Database()
    if not db.sql_fetchone(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    if db.sql_fetchone(sql=f'select admin from user_table where tg_id = {message.from_user.id}') == "0":
        await message.answer("Доступ только для администраторов")
    else:
        await message.delete()
        await message.answer(f"Панель управления лакеем\n\n"
                             f"Здесь вы можете управлять заявками", reply_markup=admin_keyboard)


async def exit_admin_menu(message: types.message):
    db = database.Database()
    if not db.sql_fetchone(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    elif not db.sql_fetchone(sql=f'select admin from user_table where tg_id = {message.from_user.id}'):
        await message.answer("Доступ только для администраторов", reply_markup=main_kb)
    else:
        await message.answer("Выход", reply_markup=main_kb)


def register_admin_menu(dp: Dispatcher):
    dp.register_message_handler(enter_admin_menu, text="👮 Управление")
    dp.register_message_handler(exit_admin_menu, text="Выйти")
