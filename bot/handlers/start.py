from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, user_service: UserService) -> None:
    
    try:
        user = await user_service.register_user(telegram_id=message.from_user.id, username=message.from_user.username)

        if user:
            await message.answer(f"You were registred")

        else:
            await message.answer(f"You have already registred in base")

    except Exception as e:
        logger.exception(f"Error {e}")
        await message.answer(f"Error on registration")


