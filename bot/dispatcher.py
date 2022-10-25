from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from bot.config import BOT_TOKEN_TEST
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=BOT_TOKEN_TEST, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())
