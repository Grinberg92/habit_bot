import asyncio
import logging
from aiogram import Bot, Dispatcher
from database.connection import pool
from bot.routers import setup_routers
from config.config import bot_settings, log_settings
from bot.middlewares.services import UserServicesMiddleware, TaskServicesMiddleware
from core.conteiner import container


async def main():

    try:

        logging.basicConfig(level=log_settings.LOG_LEVEL, format=log_settings.LOG_FORMAT)

        await pool.open()

        bot = Bot(token=bot_settings.BOT_TOKEN)
        
        dp = Dispatcher()

        dp.update.middleware(middleware=UserServicesMiddleware(
            user_service=container.user_service
        ))
        dp.update.middleware(middleware=TaskServicesMiddleware(
            task_service=container.task_service
        ))
        
        dp.include_routers(setup_routers())
        
        await dp.start_polling(bot)

    finally:

        await pool.close()

if __name__ == '__main__':
    asyncio.run(main())