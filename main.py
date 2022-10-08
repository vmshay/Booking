from aiogram.utils import executor
from bot.dispatcher import dp
import handlers.admin.admin_menu


if __name__ == '__main__':
    handlers.user.registration.register_handlers(dp)
    handlers.start.main_register(dp)
    handlers.user.events.events_register(dp)
    handlers.admin.admin_menu.register_admin_menu(dp)
    handlers.admin.manage_users.admin_handlers(dp)
    executor.start_polling(dp, skip_updates=True)

