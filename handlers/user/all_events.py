from aiogram import types, Dispatcher
from bot import database, sql
from bot.functions import beauty_all_events, date_range
from bot.keyboards import events_range_kb


async def all_events(call: types.CallbackQuery):
    await call.message.edit_text("Выберете интересующий диапазон", reply_markup=events_range_kb())


async def select_range(call: types.CallbackQuery):
    if call.data == "today":
        db = database.Database()
        time = "'" + str(date_range("today")) + "'"
        data = db.sql_fetchall(sql=sql.get_all_events(time))
        if len(data) == 0:
            await call.message.answer("Сегодня мероприятий нет")
        else:
            await call.message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))

    if call.data == "week":
        db = database.Database()
        time = date_range("week").split(" ")
        time = "'" + time[0] + "' " + time[1] + " '" + time[2] + "'"
        data = db.sql_fetchall(sql=sql.get_range_events(time))
        if len(data) == 0:
            await call.message.answer("На этой неделе мероприятий нет")
        else:
            await call.message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))

    if call.data == "month":
        db = database.Database()
        time = date_range("month").split(" ")
        time = "'" + time[0] + "' " + time[1] + " '" + time[2] + "'"
        data = db.sql_fetchall(sql=sql.get_range_events(time))
        if len(data) == 0:
            await call.message.answer("В этом месяце мероприятий нет")
        else:
            await call.message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))


def register(dp: Dispatcher):
    dp.register_callback_query_handler(all_events, text='all_events')
    dp.register_callback_query_handler(select_range, text=(['month', 'week', 'today']))