from aiogram import types, Dispatcher
from bot import database
from bot.keyboards import register_kb, make_calendar, events_range_kb
from bot.functions import make_date, date_range, beauty_all_events


async def make_event(message: types.message):
    db = database.Database()
    if not db.sql_fetchone(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(f"select approved from user_table where tg_id={message.from_user.id}"):
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


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_callback_query_handler(select_date, text_startswith='date_')

