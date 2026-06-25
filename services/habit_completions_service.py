import logging
from database.repositories.habit_completions_repository import HabitCompletionRepository
from database.models.habit_completions import HabitCompletion


class HabitCompletionService:

    def __init__(self, habit_completion_repo: HabitCompletionRepository) :
        self.habit_completion_repo = habit_completion_repo

    async def done_habit(self, habit_id: int) -> HabitCompletion | None:

        habit_completion = await self.habit_completion_repo.done_habit(habit_id=habit_id)

        if not habit_completion:
            return None
      
        return habit_completion