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
from core.scheduler import scheduler
from services.schaduler_service import SchedulerService

async def main():

    try:

        logging.basicConfig(level=log_settings.LOG_LEVEL, format=log_settings.LOG_FORMAT)

        storage = RedisStorage(redis=redis)
        await pool.open()

        bot = Bot(token=bot_settings.BOT_TOKEN)
        
        dp = Dispatcher(storage=storage)

        await SchedulerService.load_habits(bot=bot)

        dp.update.middleware(middleware=DatabaseMiddleware())

        dp.update.middleware(middleware=ServicesMiddleware())
        
        dp.include_routers(setup_routers())

        scheduler.start()
        
        await dp.start_polling(bot)

    finally:

        await pool.close()

if __name__ == '__main__':
    asyncio.run(main())