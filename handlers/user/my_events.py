from aiogram import types, Dispatcher


async def my_events(call: types.CallbackQuery):
    
    await call.message.answer("Мои события")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(my_events, text_startswith='my_events')
