from aiogram import BaseMiddleware
from typing import Any, Callable, Awaitable
from services.user_service import UserService
from services.task_service import TaskService
from database.repositories.tasks_repository import TaskRepository
from database.repositories.user_repository import UserRepository
from database.repositories.habits_repository import HabitRepository
from database.repositories.habit_completions_repository import HabitCompletionRepository
from services.habit_service import HabitService
from services.habit_completions_service import HabitCompletionService

class ServicesMiddleware(BaseMiddleware):

    async def __call__(self,
                handler: Callable[
                        [Any, dict[str, Any]],
                        Awaitable[Any]],
                event: Any,
                data: dict[str, Any]
                ):
        
        conn = data['conn']
        data['user_service'] = UserService(user_repo=UserRepository(conn))
        data['task_service'] = TaskService(task_repo=TaskRepository(conn))
        data['habit_service'] = HabitService(habit_repo=HabitRepository(conn))
        data['habit_completion_service'] = HabitCompletionService(habit_completion_repo=HabitCompletionRepository(conn))

        return await handler(event, data)
