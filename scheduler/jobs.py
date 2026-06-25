from aiogram import Bot
from bot.keyboards.habits_kb import done_habit_keyboard
from services.habit_service import HabitService

async def send_reminder(bot: Bot, habit_id: int, habit_service: HabitService):

    habit = await habit_service.get_habit_by_id(habit_id)

    await bot.send_message(chat_id=habit.user_id, 
                           text=f"🔔 Напоминание\n\n{habit.title}",
                           reply_markup=done_habit_keyboard(
                               habit_id=habit_id
                           ))