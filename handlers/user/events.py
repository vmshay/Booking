from aiogram import types, Dispatcher
from bot import database
from bot.keyboards import register_kb, make_calendar, events_range_kb
from bot.functions import make_date, date_range


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


async def my_events(message: types.Message):
    db = database.Database()
    if not db.sql_simple_check(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_simple_check(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        events = db.sql_parse_user_events(
            f"select description,`dat` from events_table WHERE owner = {message.from_user.id}")
        await message.answer("Список событий которые Вы запланировали")
        for event in events:
            await message.answer(event)
            # await message.answer(beauty_all_events(event))


async def all_events(message: types.Message):
    db = database.Database()
    if not db.sql_simple_check(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_simple_check(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        await message.answer("Укажите диапазон дат или выберите кнопкой", reply_markup=events_range_kb())


async def select_range(call: types.CallbackQuery):
    if call.data == "today":
        await call.message.answer(date_range(call.data))
    if call.data == "week":
        await call.message.answer(date_range(call.data))
    if call.data == "month":
        await call.message.answer(date_range(call.data))


        # events = db.sql_parse_all_events(f"select events_table.description, user_table.name, events_table.dat from events_table inner join user_table on events_table.owner = user_table.tg_id")


#        await message.answer("Список всех событий")
#        for event in events:
#           await message.answer(beauty_all_events(event))


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_message_handler(my_events, text="🗒 Мои события")
    dp.register_message_handler(all_events, text="📅 Все события")

    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(select_range, text=(['month', 'week', 'today']))
