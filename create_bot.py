from aiogram import Bot, Dispatcher
from db import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

# Create a bot instance
bot = Bot(token=config.token)

# Initialize the Dispatcher with the bot
dp = Dispatcher(bot, storage=MemoryStorage())  

# Open databases
db = DataBase()