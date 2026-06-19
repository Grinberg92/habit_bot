import asyncio
import logging
from aiogram import Bot, Dispatcher
from database.connection import pool
from bot.routers import setup_routers
from config.config import bot_settings, log_settings
from bot.middlewares.services import ServicesMiddleware
from bot.middlewares.database import DatabaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from core.redis import redis

async def main():

    try:

        logging.basicConfig(level=log_settings.LOG_LEVEL, format=log_settings.LOG_FORMAT)

        storage = RedisStorage(redis=redis)
        await pool.open()

        bot = Bot(token=bot_settings.BOT_TOKEN)
        
        dp = Dispatcher(storage=storage)

        dp.update.middleware(middleware=DatabaseMiddleware())

        dp.update.middleware(middleware=ServicesMiddleware())
        
        dp.include_routers(setup_routers())
        
        await dp.start_polling(bot)

    finally:

        await pool.close()

if __name__ == '__main__':
    asyncio.run(main())