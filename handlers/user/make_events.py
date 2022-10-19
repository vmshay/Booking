import asyncio
import aiogram
from aiogram import types, Dispatcher
from bot import database, sql
from bot.keyboards import register_kb, make_calendar, events_kb, cancel_booking, main_kb
from bot.functions import make_date, date_range, time_validator, normalize_time, to_quotes, check_overlap, beauty_booked_time
from handlers.user.states import BookingState
from aiogram.dispatcher.storage import FSMContext
from bot import messages
from handlers.admin.notifications import new_event
import datetime


async def make_event(message: types.message):
    db = database.Database()
    if not db.sql_fetchone(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer(messages.non_register, reply_markup=register_kb)
    else:
        if message.text == "🎯 Запланировать мероприятие":
            await message.delete()
            # TODO: Добавить переход на следующий месяц
            msg = await message.answer(messages.events_welcome(make_date()), reply_markup=make_calendar())
            await asyncio.sleep(60)
            await msg.delete()


async def select_date(call: types.CallbackQuery, state: FSMContext):
    db = database.Database()
    date = call.data.split("_")[1]
    booked = db.sql_fetchall(sql.sql_booked_time(date))
    today = datetime.datetime.now()
    if date >= datetime.datetime.strftime(today, '%Y-%m-%d'):
        if len(booked) == 0:
            await BookingState.start.set()
            await state.update_data(date=to_quotes(date))
            await state.update_data(owner=call.from_user.id)
            msg = await call.message.edit_text(f"Вы выбрали дату: {date}\n"
                                               f"На этот день мероприятий не запланированно", reply_markup=events_kb())
            await asyncio.sleep(30)
            await msg.delete()
        else:
            await BookingState.start.set()
            await state.update_data(date=to_quotes(date))
            await state.update_data(owner=call.from_user.id)
            msg = await call.message.edit_text(f"Вы выбрали дату: {date}\n\n"
                                               f"Занятое время\n\n"
                                               f"{beauty_booked_time(sorted(booked, key=lambda t: t['e_start'], reverse=False))}",
                                               reply_markup=events_kb())
            await asyncio.sleep(60)
            await msg.delete()
    else:
        msg = await call.message.answer("Нельзя выбрать дату позже сегодняшней")
        await asyncio.sleep(5)
        await msg.delete()


async def edit_date(call: types.CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(f"выберите дату чтобы увидеть список мероприятий\n\n"
                                       f"Так же календарь мероприятий можно посмотреть в "
                                       f"<a href=moodle.tomtit-tomsk.ru>Moodle</a>\n\n"
                                       f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar())
    await call.message.delete()
    await state.finish()
    await asyncio.sleep(30)
    await msg.delete()


async def booking_date(call: types.CallbackQuery):
    msg = await call.message.answer("Введите диапазон времени\n"
                                    "Возможные форматы\n\n"
                                    "13.00 15.30\n"
                                    "13.00-15.30\n"
                                    "13:00 15:30\n"
                                    "13.00-15.30\n", reply_markup=cancel_booking())
    await BookingState.time.set()
    await asyncio.sleep(20)
    await msg.delete()


async def get_time(message: types.Message, state: FSMContext):
    # Парсим то что ввел пользователь
    time = normalize_time(message.text)
    await message.delete()
    # Забираем текущую дату
    date = await state.get_data()
    # Проверяем валидность времени
    if time_validator(message.text):
        # Проверяем что старт не позже конца
        if time[0] > time[1]:
            msg = await message.answer("Начало не может быть раньше конца")
            await asyncio.sleep(5)
            await msg.delete()
        elif not check_overlap(time[0], time[1], date['date']):
            msg = await message.answer("Указанное время пеерсекается")
            await asyncio.sleep(5)
            await msg.delete()
        else:
            await state.update_data(t_start=time[0])
            await state.update_data(t_end=time[1])
            await BookingState.description.set()
            msg = await message.answer("Введите краткое описание мероприятия", reply_markup=cancel_booking())
            await asyncio.sleep(10)
            await msg.delete()
    else:
        msg = await message.answer("Неверный формат времени")
        await asyncio.sleep(5)
        await msg.delete()


async def send_event(message: types.Message, state: FSMContext):
    db = database.Database()
    if len(message.text) > 100:
        msg = await message.answer("Описание слишком длинное")
        await asyncio.sleep(5)
        await msg.delete()
        await message.delete()
    else:
        await state.update_data(description=message.text)
        await state.update_data(approved=0)
        data = await state.get_data()
        await message.delete()
        msg = await message.answer("Заявка принята", reply_markup=main_kb)
        await asyncio.sleep(5)
        await msg.delete()
        await state.finish()
        db.sql_query_send(sql.sql_send_event(data))
        await new_event()


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(edit_date, text=['change', 'cancel_booking'], state=[BookingState.start,
                                                                                            BookingState.time,
                                                                                            BookingState.description])
    dp.register_callback_query_handler(booking_date, text='booking', state=BookingState.start)
    dp.register_message_handler(get_time, state=BookingState.time)
    dp.register_message_handler(send_event, state=BookingState.description)
