from aiogram.utils import executor
from bot.dispatcher import dp
import handlers.admin.admin_menu
import logging
from Moodle.scheduler import on_start


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    handlers.user.registration.register_handlers(dp)
    handlers.user.make_events.events_register(dp)
    handlers.user.show_events.register(dp)
    handlers.admin.admin_menu.register_admin_menu(dp)
    handlers.admin.manage_users.admin_handlers(dp)
    handlers.admin.manage_events.register_handlers(dp)
    handlers.start.main_register(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
