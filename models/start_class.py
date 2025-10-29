import os
from aiogram import Dispatcher, Router as AiogramRouter, Bot
from aiogram.types import CallbackQuery
from aiogram.filters import Filter
from models.log_class import LogCLassAll
from dotenv import load_dotenv

load_dotenv()

class RouterStore:
    my_router = AiogramRouter()

class StartBot:
    def __init__(self):
        self.dp = Dispatcher()
        self.dp.include_router(RouterStore.my_router)
        LogCLassAll().info("Start bot")

    async def run(self):
        await self.dp.start_polling(InstanceBot.bot)
    
class CallbackDataFilter(Filter):
    def __init__(self, data: str) -> None:
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.data
    
class InstanceBot:
    TOKEN = os.getenv("TOKEN")
    bot = Bot(token=TOKEN)