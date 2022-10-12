from aiogram import types, Dispatcher
from bot import database
from bot.keyboards import register_kb, make_calendar, events_range_kb
from bot.functions import make_date, date_range, beauty_all_events


async def make_event(message: types.message):
    db = database.Database()
    if not db.sql_simple_check(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        if message.text == "🎯 Запланировать мероприятие":
            await message.delete()
            await message.answer(f"выберите дату чтобы увидеть список мероприятий\n\n"
                                 f"Так же календарь мероприятий можно посмотреть в "
                                 f"<a href=moodle.tomtit.tomsk.ru>Moodle</a>\n\n"
                                 f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar())


async def select_date(call: types.CallbackQuery):
    await call.message.answer(call.data)
    # TODO: Планирование по дате


async def my_events(message: types.Message):
    db = database.Database()
    if db.sql_simple_check(sql=f'select admin from user_table where tg_id = {message.from_user.id}') == "0":
        await message.answer("В разработке")
    elif not db.sql_simple_check(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_simple_check(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        data = db.sql_fetchall(sql=f"select events_table.description, user_table.name, events_table.e_date "
                                   f"from events_table inner join user_table "
                                   f"on events_table.owner = user_table.tg_id "
                                   f"where events_table.owner={message.from_user.id}")

        if len(data) == 0:
            await message.answer("Вы не планировали мероприятия")
        else:
            await message.answer(data)


async def all_events(message: types.Message):
    db = database.Database()
    if db.sql_simple_check(sql=f'select admin from user_table where tg_id = {message.from_user.id}') == "0":
        await message.answer("В разработке")
    elif not db.sql_simple_check(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_simple_check(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        await message.answer("Выберете интересующий диапазон", reply_markup=events_range_kb())


async def select_range(call: types.CallbackQuery):
    if call.data == "today":
        db = database.Database()
        time = "'"+str(date_range("today"))+"'"
        data = db.sql_fetchall(sql=f"select events_table.description, user_table.name, events_table.e_date "
                                   f"from events_table inner join user_table "
                                   f"on events_table.owner = user_table.tg_id "
                                   f"where events_table.e_date={time}")

        if len(data) == 0:
            await call.message.answer("Сегодня мероприятий нет")
        else:
            await call.message.answer(data)

    if call.data == "week":
        db = database.Database()
        time = date_range("week").split(" ")
        time = "'" + time[0] + "' " + time[1] + " '" + time[2] + "'"
        data = db.sql_fetchall(sql=f"select events_table.description, user_table.name, events_table.e_date "
                                   f"from events_table inner join user_table "
                                   f"on events_table.owner = user_table.tg_id "
                                   f"where events_table.e_date between {time}")

        if len(data) == 0:
            await call.message.answer("На этой неделе мероприятий нет")
        else:
            await call.message.answer(data)
            print(data)
            new_data = sorted(data,key=lambda d: d['e_date'])
            print(new_data)
            await call.message.answer(new_data)

    if call.data == "month":
        db = database.Database()
        time = date_range("month").split(" ")
        time = "'" + time[0] + "' " + time[1] + " '" + time[2] + "'"
        data = db.sql_fetchall(sql=f"select events_table.description, user_table.name, events_table.e_date "
                                   f"from events_table inner join user_table "
                                   f"on events_table.owner = user_table.tg_id "
                                   f"where events_table.e_date between {time}")
        await call.message.answer(data)



def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_message_handler(my_events, text="🗒 Мои события")
    dp.register_message_handler(all_events, text="📅 Все события")

    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(select_range, text=(['month', 'week', 'today']))
