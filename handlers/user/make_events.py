from aiogram import types, Dispatcher
from bot import database
from bot.keyboards import register_kb, make_calendar, events_kb, cancel_booking
from bot.functions import make_date
from handlers.user.states import BookingState
from aiogram.dispatcher.storage import FSMContext


async def make_event(message: types.message):
    db = database.Database()
    if not db.sql_fetchone(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        if message.text == "🎯 Запланировать мероприятие":
            await message.delete()
            # TODO: Добавить переход на следующий месяц
            await message.answer(f"выберите дату чтобы увидеть список мероприятий\n\n"
                                 f"Так же календарь мероприятий можно посмотреть в "
                                 f"<a href=moodle.tomtit.tomsk.ru>Moodle</a>\n\n"
                                 f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar())


async def select_date(call: types.CallbackQuery):
    db = database.Database()
    print(call.data)
    # TODO: Планирование по дате
    # Показать занятое время в выбраный день
    time = "'" + call.data.split("_")[1] + "'"
    booked = db.sql_fetchall(f"select events_table.e_start, events_table.e_end from events_table WHERE e_date = {time}")
    await BookingState.start.set()
    if len(booked) == 0:
        await call.message.edit_text("На этот день мероприятий не заплпнированно", reply_markup=events_kb())
    else:
        await call.message.edit_text(sorted(booked, key=lambda t: t['e_start'], reverse=True), reply_markup=events_kb())


async def edit_date(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"выберите дату чтобы увидеть список мероприятий\n\n"
                                 f"Так же календарь мероприятий можно посмотреть в "
                                 f"<a href=moodle.tomtit.tomsk.ru>Moodle</a>\n\n"
                                 f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar())
    print("Отменено")
    await state.finish()


async def booking_date(call: types.CallbackQuery):
    print(call.message.text)
    await call.message.edit_text("введите время", reply_markup=cancel_booking())
    await BookingState.time.set()


async def get_date(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Введите краткое описание мероприятия", reply_markup=cancel_booking())
    await BookingState.description.set()


async def send_event(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    print(data)
    await state.finish()


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_callback_query_handler(select_date, text_startswith='date_')
    dp.register_callback_query_handler(edit_date, text=['change', 'cancel_booking'], state=[BookingState.start,
                                                                                            BookingState.time,
                                                                                            BookingState.description])
    dp.register_callback_query_handler(booking_date, text='booking',state=BookingState.start)
    dp.register_message_handler(get_date, state=BookingState.time)
    dp.register_message_handler(send_event,state=BookingState.description)
