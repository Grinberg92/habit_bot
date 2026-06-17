import asyncio
from aiogram import Bot, Dispatcher
from database.connection import pool
from bot.routers import setup_routers
from config.config import db_settings, bot_settings


async def main():
    bot = Bot(token=bot_settings.BOT_TOKEN)
    
    dp = Dispatcher()
    
    dp.include_routers(setup_routers())
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())