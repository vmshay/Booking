from aiogram import types, Dispatcher
from bot.keyboards import main_kb

async def start_cmd(message: types.Message):
    if message.chat.type == 'private':
        # TODO: Проверка регистрации
        msg = "🤖Вас приветствует бот 405 аудитории🤖\n\n"
        msg += "C моей помощью Вы можете забронировать мероприятие\n\n"
        msg += "Если есть преддоженния или замечания обратитесь к @FeldwebelWillman"
        await message.answer(msg,reply_markup=main_kb())
    else:
        await message.answer(f"Если Вы хотите оставить заявку, "
                             f"напишите лично мне")


def register(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
