import logging

from aiogram import executor
from bot.dispatcher import dp
import handlers

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handlers.commands.register(dp)
    executor.start_polling(dp, skip_updates=True)
