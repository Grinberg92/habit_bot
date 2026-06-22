from aiogram import Bot

async def send_reminder(bot: Bot, user_id: int, text: str):

    await bot.send_message(chat_id=user_id, text=f"🔔 Напоминание\n\n{text}")