# @dp.callback_query_handler(text_contains='menu_1')
# async def menu(call: types.CallbackQuery):
#     await bot.answer_callback_query(call.id)
#     await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=make_keyboard()
#
#
# @dp.callback_query_handler(text='menu_4')
# async def xyi(call: types.CallbackQuery):
#     await bot.answer_callback_query(call.id)
#     await bot.send_message(call.from_user.id, text="пошел нахуй со своим расписанием")


# Класс состояний для бронирования
# from aiogram.dispatcher.filters.state import StatesGroup, State
# class BookingState(StatesGroup):
#     owner = State()
#     time = State()
#     description = State()
#     group = State()
#     persons = State()




# async def user_manage(message: types.Message):
#     if not sql_check_user(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
#             not sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}", "approved"):
#         await message.delete()
#         await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
#     elif not sql_simple_check(f'select admin from user_table where tg_id = {message.from_user.id}', "admin"):
#         await message.answer("Доступ только для администраторов", reply_markup=main_kb)
#     else:
#         await message.answer(f"Управление пользователями\n\n"
#                              f"Здесь вы можете управлять заявками на регистрацию\n\n")
#         if not sql_check_user(f"select name,phone from user_table where approved = '0'"):
#             await message.answer("Нет заявок на регистрацию")
#         else:
#             data = sql_parse_users(f"select id,name,phone from user_table where approved = '0'")
#             await message.answer(f"Заявки на регистрацию")
#             await message.answer(" ".join(sql_parse_users(f"select id,name,phone from user_table where approved = '0'")))
#             await message.answer(''.join(data[:1]), reply_markup=kb_user_manage())


# @dp.callback_query_handler()
# async def select_date(call: types.CallbackQuery):
#     await bot.answer_callback_query(call.id)
#     await bot.send_message(call.message.chat.id, "Вы выбрали " + call.data)