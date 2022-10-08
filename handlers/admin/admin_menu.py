from aiogram import types, Dispatcher
from database import sql_simple_check, sql_check_user
from keyboards import register_kb, main_kb, admin_keyboard


async def enter_admin_menu(message: types.message):
    if not sql_check_user(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}", "approved"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    elif not sql_simple_check(f'select admin from user_table where tg_id = {message.from_user.id}', "admin"):
        await message.answer("Доступ только для администраторов")
    else:
        await message.delete()
        await message.answer(f"Панель управления лакеем\n\n"
                             f"Здесь вы можете управлять заявками", reply_markup=admin_keyboard)


async def exit_admin_menu(message: types.message):
    if not sql_check_user(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}", "approved"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    elif not sql_simple_check(f'select admin from user_table where tg_id = {message.from_user.id}', "admin"):
        await message.answer("Доступ только для администраторов", reply_markup=main_kb)
    else:
        await message.answer("Выход", reply_markup=main_kb)


def register_admin_menu(dp: Dispatcher):
    dp.register_message_handler(enter_admin_menu, text="👮 Управление")
    dp.register_message_handler(exit_admin_menu, text="Выйти")
