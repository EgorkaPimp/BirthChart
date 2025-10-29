from aiogram import types
from aiogram.filters import Command, CommandObject

from models.start_class import RouterStore
from models.log_class import LogCLassAll

@RouterStore.my_router.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    LogCLassAll().info('Write command: Start')
    