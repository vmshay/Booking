from bot import database
from aiogram import types, Dispatcher
from bot.keyboards import register_kb, events_range_kb
from bot.functions import date_range, beauty_all_events
from bot import sql


async def my_events(message: types.Message):
    await message.delete()
    db = database.Database()
    if db.sql_fetchone(sql=sql.check_approved(message.from_user.id)) == "0" or db.sql_fetchone(
            sql=sql.check_id(message.from_user.id)) == "0":
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        data = db.sql_fetchall(sql=sql.get_user_event(message.from_user.id))
        if len(data) == 0:
            await message.answer("Вы не планировали мероприятия")
        else:
            await message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))


async def all_events(message: types.Message):
    await message.delete()
    db = database.Database()
    if db.sql_fetchone(sql=sql.check_approved(message.from_user.id)) == "0" or db.sql_fetchone(
            sql=sql.check_id(message.from_user.id)) == "0":
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        await message.answer("Выберете интересующий диапазон", reply_markup=events_range_kb())


# TODO: Визуальное оформление событий


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

        await call.message.answer(beauty_all_events(sorted(data, key=lambda d: d['e_date'])))


def register(dp: Dispatcher):
    dp.register_message_handler(my_events, text="🗒 Мои события")
    dp.register_message_handler(all_events, text="📅 Все события")
    dp.register_callback_query_handler(select_range, text=(['month', 'week', 'today']))
