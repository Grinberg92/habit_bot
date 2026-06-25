import logging
from database.repositories.habits_repository import HabitRepository
from database.models.habits import Habit

logger = logging.getLogger(__name__)

class HabitService:

    def __init__(self, habit_repo: HabitRepository):
        self.habit_repo = habit_repo

    async def create_habit(self, user_id: int, title: str, reminder_time: str) -> Habit | None:

        habit = await self.habit_repo.create_habit(user_id=user_id, title=title, reminder_time=reminder_time)

        if not habit:
            return None
      
        return habit
    
    async def get_habit_by_user(self, user_id: int) -> tuple[Habit]:

        habits = await self.habit_repo.get_habits_by_user(user_id=user_id)

        return habits

    async def get_habit_by_id(self, habit_id:int) -> Habit | None:

        habit = await self.habit_repo.get_habit_by_id(habit_id)

        return habit
    
    async def get_active_habits(self) -> tuple[Habit]:

        habits = await self.habit_repo.get_active_habits()

        return habits

    async def set_active_habit(self, habit_id: int, is_active: bool) -> bool:

        updated = await self.habit_repo.set_active_habit(habit_id=habit_id, is_active=is_active)
        
        return updated > 0
    
    async def delete_habit(self, habit_id:int) -> bool:

        deleted = await self.habit_repo.delete_habit(habit_id)


        if deleted:
            return True


        return False
    
    async def update_habit_title(self, habit_id: int, title: str) -> bool:

        updated = await self.habit_repo.update_habit_title(habit_id=habit_id, title=title)
        
        return updated > 0
    
    async def update_habit_time(self, habit_id: int, time: str) -> bool:

        updated = await self.habit_repo.update_habit_time(habit_id=habit_id, time=time)
        
        return updated > 0