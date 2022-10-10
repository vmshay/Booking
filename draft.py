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
#            await message.answer(" ".join(sql_parse_users(f"select id,name,phone"
#                                                          f"from user_table"
#                                                          f"where approved = '0'")))
#             await message.answer(''.join(data[:1]), reply_markup=kb_user_manage())


# @dp.callback_query_handler()
# async def select_date(call: types.CallbackQuery):
#     await bot.answer_callback_query(call.id)
#     await bot.send_message(call.message.chat.id, "Вы выбрали " + call.data)

        # events = db.sql_parse_all_events(f"select events_table.description, user_table.name, events_table.dat from events_table inner join user_table on events_table.owner = user_table.tg_id")


#        await message.answer("Список всех событий")
#        for event in events:
#           await message.answer(beauty_all_events(event))
