import asyncio
import calendar
from datetime import date, datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from bot import database, sql
from bot.functions import make_date, time_validator, normalize_time, to_quotes, check_overlap, beauty_booked_time
from bot.keyboards import make_calendar, events_kb, cancel_booking, main_kb
from bot.notifications import new_event
from bot.states import BookingState


async def make_event(call: types.CallbackQuery):

    today = date.today()
    month = today.month
    days_in_month = calendar.monthrange(today.year, month)[1]
    db = database.Database()
    text = (f"выберите дату чтобы увидеть список мероприятий\n\n"
            f"Так же календарь мероприятий можно посмотреть в "
            f"<a href=moodle.tomtit-tomsk.ru>Moodle</a>\n\n"
            f"Сегодняшняя дата <b>{make_date()}</b>")
    await call.message.edit_text(text, reply_markup=make_calendar(month,
                                                                  days_in_month,
                                                                  f"month_prev:{month}",
                                                                  f"month_next:{month}"))


async def select_date(call: types.CallbackQuery, state: FSMContext):
    db = database.Database()
    username = db.sql_fetchone(f"select name from user_table where tg_id = {call.from_user.id}")
    await state.update_data(username=username)
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
    await call.message.edit_text(f"🤖Вас приветствует бот 405 кабинета🤖\n"
                                 f"Я помогу Вам запланировать мероприятие.\n\n"
                                 f"Вот что можно сделать:\n"
                                 f"<b>Запланировать мероприятие</b>\n"
                                 f"Планирование мероприятия\n\n"
                                 f"<b>Мои события</b>\n"
                                 f"События запланированные Вами\n\n"
                                 f"<b>Все события</b>\n"
                                 f"События всех пользователей\n"
                                 f"с выборкой по интервалам\n\n"
                                 f"Если есть пожелания или замечания\n"
                                 f"Можете обратиться к @FeldwebelWillman\n"
                                 f"Или воспользовтаься обратной связью /feedback",
                                 reply_markup=main_kb())
    await state.finish()


async def booking_date(call: types.CallbackQuery):
    await call.message.edit_text("Введите диапазон времени\n"
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
        db.sql_query_send(sql.sql_send_event(data))
        await message.delete()
        await message.answer("Заявка принята\n"
                             "Уведомлять администраторов не требуется\n"
                             "они получат оповощение автоматически\n"
                             "Для новой заявки используйте /start")
        event_id = db.sql_fetchone('select max(id) from events_table')
        await state.update_data(id=event_id)
        data = await state.get_data()
        await state.finish()
        await new_event(data)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(make_event, text='plain')
    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(edit_date, text='cancel_booking')
    dp.register_callback_query_handler(booking_date, text='booking', state=BookingState.start)
    dp.register_callback_query_handler(edit_date, text=['change', 'cancel_booking'], state=[BookingState.start,
                                                                                            BookingState.time,
                                                                                            BookingState.description])

    dp.register_message_handler(get_time, state=BookingState.time)
    dp.register_message_handler(send_event, state=BookingState.description)