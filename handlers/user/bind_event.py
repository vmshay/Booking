from aiogram import types, Dispatcher


async def bind_event(call: types.CallbackQuery):
    await call.message.answer("Тут типа евент биндить")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(bind_event, text_startswith="bind_event")
