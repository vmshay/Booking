import logging

from aiogram import executor
from bot.dispatcher import dp


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)