import logging
from database.repositories.habits_repository import HabitRepository
from database.models.habits import Habit

logger = logging.getLogger(__name__)

class HabitService:

    def __init__(self, habit_repo: HabitRepository):
        self.habit_repo = habit_repo

    async def create_habit(self, user_id: int, title: str, reminder_time: str) -> Habit | bool:

        habit = await self.habit_repo.create_habit(user_id=user_id, title=title, reminder_time=reminder_time)

        if not habit:
            return False
        
        logger.info(
            f"Habit {habit.title} created"
        )      

        return habit
    
    async def get_habit_by_user(self, user_id: int) -> tuple[Habit]:

        habits = await self.habit_repo.get_habits_by_user(user_id=user_id)

        return habits