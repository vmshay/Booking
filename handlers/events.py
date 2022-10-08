from aiogram import types, Dispatcher
from database import sql_check_user, sql_simple_check
from keyboards import register_kb, make_calendar
from functions import make_date


async def make_event(message: types.message):
    if not sql_check_user(f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not sql_simple_check(f"select approved from user_table where tg_id={message.from_user.id}", "approved"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    else:
        if message.text == "🎯 Запланировать мероприятие":

            await message.delete()
            await message.answer(f"Выберете дату чтобы увидеть список мероприятий\n\n"
                                 f"Так же календарь мероприятий можно посмотреть в "
                                 f"<a href=moodle.tomtit.tomsk.ru>Moodle</a>\n\n"
                                 f"Сегодняшняя дата <b>{make_date()}</b>", reply_markup=make_calendar())
            msg = await message.answer("asd")
            print(msg)


async def select_date(call: types.CallbackQuery):
    await call.message.answer(call.data)


async def my_events(message: types.Message):
    await message.answer("")


async def all_events(message: types.Message):
    await message.answer("")


def events_register(dp: Dispatcher):
    dp.register_message_handler(make_event, text="🎯 Запланировать мероприятие")
    dp.register_message_handler(my_events, text="🗒 ️Мои события")
    dp.register_message_handler(all_events, text="📅 Все события")

    dp.register_callback_query_handler(select_date, text_startswith='date_')
