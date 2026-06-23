import logging

from aiogram import Bot
from database.connection import pool
from core.scheduler import scheduler
from database.models.habits import Habit
from database.repositories.habits_repository import HabitRepository
from scheduler.jobs import send_reminder
from services.habit_service import HabitService

logger = logging.getLogger(__name__)

class SchedulerService:


    @staticmethod
    async def load_habits(bot: Bot) -> None:

        async with pool.connection() as conn:

            habit_service = HabitService(habit_repo=HabitRepository(conn))

            habits = await habit_service.get_active_habits()

            if not habits:
                logger.info("No active habits found")
                return

            for habit in habits:

                __class__.add_habit_job(bot, habit)
                logger.info(f"loaded habit {habit.id}")

    @staticmethod
    def add_habit_job(bot: Bot, habit: Habit) -> None:

        scheduler.add_job(
            send_reminder,
            trigger='cron',
            hour=habit.reminder_time.hour,
            minute=habit.reminder_time.minute,
            kwargs={
                "bot": bot,
                "user_id": habit.user_id,
                "text": habit.title
                },
            id=f"habit_{habit.id}",
            replace_existing=True
        ) 

    @staticmethod
    def delete_job(habit_id: int) -> None:

        job_id = f"habit_{habit_id}"

        job = scheduler.get_job(job_id=job_id)

        if job:

            scheduler.remove_job(job_id=job_id)

            logger.info(
                f"Removed job {job_id}"
            )