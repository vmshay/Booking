import asyncio
from aiogram import types, Dispatcher
from bot import database, sql
from bot.keyboards import register_kb, make_calendar, events_kb, cancel_booking, main_kb
from bot.functions import make_date, time_validator, normalize_time, to_quotes, check_overlap, beauty_booked_time
from handlers.user.states import BookingState
from aiogram.dispatcher.storage import FSMContext
from bot import messages
from handlers.admin.notifications import new_event
from datetime import date, datetime
import calendar


async def make_event(message: types.message):
    today = date.today()
    month = today.month
    days_in_month = calendar.monthrange(today.year, month)[1]
    db = database.Database()
    if not db.sql_fetchone(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer(messages.non_register, reply_markup=register_kb)
    else:
        if message.text == "🎯 Запланировать мероприятие":
            await message.delete()
            await message.answer(messages.events_welcome(make_date()), reply_markup=make_calendar(month,
                                                                                                  days_in_month,
                                                                                                  f"month_prev:{month}",
                                                                                                  f"month_next:{month}"))


async def select_date(call: types.CallbackQuery, state: FSMContext):
    db = database.Database()
    date = call.data.split("_")[1]
    booked = db.sql_fetchall(sql.sql_booked_time(date))
    today = datetime.strftime(datetime.today(), '%Y-%m-%d')
    t_day = today.split("-")[2]
    t_month = today.split("-")[1]

    if int(date.split("-")[1]) == int(t_month):
        if int(date.split("-")[2]) >= int(t_day):
            if len(booked) == 0:
                await BookingState.start.set()
                await state.update_data(date=to_quotes(date))
                await state.update_data(owner=call.from_user.id)
                await call.message.edit_text(f"Вы выбрали дату: {date}\n"
                                             f"На этот день мероприятий не запланированно", reply_markup=events_kb())
            else:
                await BookingState.start.set()
                await state.update_data(date=to_quotes(date))
                await state.update_data(owner=call.from_user.id)
                await call.message.edit_text(f"Вы выбрали дату: {date}\n\n"
                                             f"Занятое время\n\n"
                                             f"{beauty_booked_time(sorted(booked, key=lambda t: t['e_start'], reverse=False))}",
                                             reply_markup=events_kb())
        else:
            msg = await call.message.answer("Нельзя выбрать дату позже сегодняшней")
            await asyncio.sleep(5)
            await msg.delete()
    elif int(date.split("-")[1]) > int(t_month):
        if len(booked) == 0:
            await BookingState.start.set()
            await state.update_data(date=to_quotes(date))
            await state.update_data(owner=call.from_user.id)
            await call.message.edit_text(f"Вы выбрали дату: {date}\n"
                                         f"На этот день мероприятий не запланированно", reply_markup=events_kb())
        else:
            await BookingState.start.set()
            await state.update_data(date=to_quotes(date))
            await state.update_data(owner=call.from_user.id)
            await call.message.edit_text(f"Вы выбрали дату: {date}\n\n"
                                         f"Занятое время\n\n"
                                         f"{beauty_booked_time(sorted(booked, key=lambda t: t['e_start'], reverse=False))}",
                                         reply_markup=events_kb())
    else:
        msg = await call.message.answer("Нельзя выбрать дату позже сегодняшней")
        await asyncio.sleep(5)
        await msg.delete()


async def edit_date(call: types.CallbackQuery, state: FSMContext):
    today = date.today()
    month = today.month
    days_in_month = calendar.monthrange(today.year, month)[1]
    await call.message.edit_text(f"выберите дату чтобы увидеть список мероприятий\n\n"
                                 f"Так же календарь мероприятий можно посмотреть в "
                                 f"<a href=moodle.tomtit-tomsk.ru>Moodle</a>\n\n"
                                 f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar(month,
                                                                                                      days_in_month,
                                                                                                      f"month_prev:{month}",
                                                                                                      f"month_next:{month}"))

    await state.finish()


async def booking_date(call: types.CallbackQuery):
    await call.message.answer("Введите диапазон времени\n"
                              "Возможные форматы\n\n"
                              "13.00 15.30\n"
                              "8.00-9.00\n"
                              "10:30 14:00\n"
                              "11.50-12.30\n", reply_markup=cancel_booking())
    await BookingState.time.set()


async def get_time(message: types.Message, state: FSMContext):
    # Парсим то что ввел пользователь
    time = normalize_time(message.text)
    await message.delete()
    date = await state.get_data()
    # Проверяем валидность времени
    if time_validator(message.text):
        # Проверяем что старт не позже конца
        if time[0] > time[1]:
            await message.answer("Начало не может быть раньше конца")
        elif not check_overlap(time[0], time[1], date['date']):
            await message.answer("Указанное время пеерсекается")

        else:
            await state.update_data(t_start=time[0])
            await state.update_data(t_end=time[1])
            await BookingState.description.set()
            await message.answer("Введите краткое описание мероприятия", reply_markup=cancel_booking())

    else:
        await message.answer("Неверный формат времени")


async def send_event(message: types.Message, state: FSMContext):
    db = database.Database()
    if len(message.text) > 100:
        await message.answer("Описание слишком длинное")

    else:
        await state.update_data(description=message.text)
        await state.update_data(approved=0)
        data = await state.get_data()
        await message.delete()
        await message.answer("Заявка принята\n"
                             "Уведомлять администраторов не требуется\n"
                             "они получат оповощение автоматически", reply_markup=main_kb)
        await state.finish()
        db.sql_query_send(sql.sql_send_event(data))
        await new_event()


async def next_month(call: types.CallbackQuery):
    m_id = int(call.data.split(":")[1])+1
    days = calendar.monthrange(2022, m_id)[1]
    await call.message.edit_reply_markup(reply_markup=make_calendar(m_id,
                                                                    days,
                                                                    f"month_prev:{m_id}",
                                                                    f"month_next:{m_id}"))


async def prev_month(call: types.CallbackQuery):
    m_id = int(call.data.split(":")[1])-1
    days = calendar.monthrange(2022, m_id)[1]
    await call.message.edit_reply_markup(reply_markup=make_calendar(m_id,
                                                                    days,
                                                                    f"month_prev:{m_id}",
                                                                    f"month_next:{m_id}"))


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(edit_date, text=['change', 'cancel_booking'], state=[BookingState.start,
                                                                                            BookingState.time,
                                                                                            BookingState.description])
    dp.register_callback_query_handler(booking_date, text='booking', state=BookingState.start)
    dp.register_message_handler(get_time, state=BookingState.time)
    dp.register_message_handler(send_event, state=BookingState.description)
    dp.register_callback_query_handler(next_month, text_startswith='month_next')
    dp.register_callback_query_handler(prev_month, text_startswith='month_prev')
