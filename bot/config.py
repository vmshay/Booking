import os
from dotenv import load_dotenv

load_dotenv()
env_path = '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
