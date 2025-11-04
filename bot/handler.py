from aiogram import types
from aiogram.filters import Command, CommandObject
from models.start_class import RouterStore
from models.log_class import LogCLassAll
from models.work_files import Images
from bot.inline import app_start

image = Images.test_image()

@RouterStore.my_router.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    LogCLassAll().info('Write command: Start')
    await message.answer_photo(photo=image,
                            caption="Bla bla bla",
                            reply_markup = app_start())