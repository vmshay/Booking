import logging

from aiogram import executor
from bot.dispatcher import dp

import handlers.user

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handlers.commands.register(dp)
    handlers.user.all_events.register(dp)
    handlers.user.my_events.register(dp)
    handlers.user.bind_event.register(dp)
    executor.start_polling(dp, skip_updates=True)


