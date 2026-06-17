from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer('Working')