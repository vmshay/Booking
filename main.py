from aiogram.utils import executor
from bot.dispatcher import dp
import handlers.admin.admin_menu
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    handlers.user.registration.register_handlers(dp)
    handlers.user.make_events.events_register(dp)
    handlers.user.show_events.register(dp)
    handlers.admin.admin_menu.register_admin_menu(dp)
    handlers.admin.manage_users.admin_handlers(dp)
    handlers.admin.manage_events.register_handlers(dp)
    handlers.start.main_register(dp)
    executor.start_polling(dp, skip_updates=True)
