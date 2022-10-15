# TODO: Добавить управление мероприятиями
from aiogram import types, Dispatcher
from bot import database
from bot.functions import parse_events
from bot.keyboards import register_kb,manage_kb
from bot import sql


async def list_events(message: types.Message):
    db = database.Database()
    if not db.sql_fetchone(sql=f"select tg_id from user_table where tg_id ={message.from_user.id}") or \
            not db.sql_fetchone(sql=f"select approved from user_table where tg_id={message.from_user.id}"):
        await message.delete()
        await message.answer("Команды станут доступны после регистрации", reply_markup=register_kb)
    events = db.sql_fetchall(sql.sql_manage_events())
    if len(events) == 0:
        await message.answer("Заявки отсутствуют")
    else:
        await message.answer(parse_events(events)[0], reply_markup=manage_kb(f"e_accept:{events[0]['id']}", f"e_deny:{events[0]['id']}", f"e_next:0",
                                                    f"e_prev:0", f"1/{len(events)}"))


async def next_event_page(call: types.CallbackQuery):
    db = database.Database()
    events = db.sql_fetchall(sql.sql_manage_events())
    index = int(call.data.split(":")[1]) + 1

    if not events:
        await call.message.answer('Заявки отсутствуют')
    if index == len(events):
        pass
        print("next")
    else:
        event_id = events[index]['id']
        await call.message.edit_text(parse_events(events)[index],
                                     reply_markup=manage_kb(f"e_accept:{event_id}", f"e_deny:{event_id}", f"e_next:{index}",
                                                            f"e_prev:{index}", f"{index + 1}/{len(events)}"))


async def prev_event_page(call: types.CallbackQuery):
    db = database.Database()

    events = db.sql_fetchall(sql.sql_manage_events())
    index = int(call.data.split(":")[1]) - 1

    if not events:
        await call.message.answer('Заявки отсутствуют')
    if index < 0:
        print(events)
        print("prev")
        pass
    else:
        event_id = events[index]['id']
        await call.message.edit_text(parse_events(events)[index],
                                     reply_markup=manage_kb(f"e_accept:{event_id}", f"e_deny:{event_id}", f"e_next:{index}",
                                                            f"e_prev:{index}", f"{index + 1 }/{len(events)}"))


async def accept_event(call: types.CallbackQuery):
    db = database.Database()
    events = db.sql_fetchall(sql.sql_manage_events())
    index = int(call.message.reply_markup.inline_keyboard[1][1].text.split("/")[0])-1

    if len(events) == 1:
        event_id = events[index]['id']
        db.sql_query_send(f"UPDATE booking.events_table SET approved='1' WHERE id={event_id}")
        await call.message.delete()
        await call.message.answer('Заявки отсутствуют')
    elif index == 0:
        event_id = events[index]['id']
        db.sql_query_send(f"UPDATE booking.events_table SET approved='1' WHERE id={event_id}")
        await call.message.edit_text(parse_events(events)[index+1],
                                     reply_markup=manage_kb(f"e_accept:{event_id}", f"e_deny:{event_id}", f"e_next:{index + 1}",
                                                            f"e_prev:{index + 1}", f"{index + 1}/{len(events) - 1}"))
    elif index == len(events)-1:
        event_id = events[index]['id']
        db.sql_query_send(f"UPDATE booking.events_table SET approved='1' WHERE id={event_id}")
        await call.message.edit_text(parse_events(events)[index-1],
                                     reply_markup=manage_kb(f"e_accept:{event_id}", f"e_deny:{event_id}", f"e_next:{index - 1}",
                                                            f"e_prev:{index - 1}", f"{index}/{len(events) - 1}"))
        print("2 " +index)
    else:
        event_id = events[index]['id']
        db.sql_query_send(f"UPDATE booking.events_table SET approved='1' WHERE id={event_id}")
        await call.message.edit_text(parse_events(events)[index+1],
                                     reply_markup=manage_kb(f"e_accept:{event_id}", f"e_deny:{event_id}", f"e_next:{index}",
                                                            f"e_prev:{index}", f"{index}/{len(events) - 1}"))
        print(event_id, index)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(list_events, text='🎫 Управление мероприятиями')
    dp.register_callback_query_handler(next_event_page, text_startswith='e_next')
    dp.register_callback_query_handler(prev_event_page, text_startswith='e_prev')
    dp.register_callback_query_handler(accept_event, text_startswith='e_accept')

