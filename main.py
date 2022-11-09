from aiogram.utils import executor
from bot.dispatcher import dp
import logging
import handlers
from Moodle.scheduler import on_start


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handlers.start.main_register(dp)
    handlers.user.registration.register(dp)
    handlers.user.make_event.register(dp)

    handlers.admin.deny_user.register(dp)
    handlers.admin.accept_user.register(dp)
    handlers.admin.accept_event.register(dp)
    handlers.admin.deny_event.register(dp)
    handlers.user.my_events.register(dp)
    handlers.user.all_events.register(dp)
    executor.start_polling(dp, skip_updates=True)  # , on_startup=on_start
