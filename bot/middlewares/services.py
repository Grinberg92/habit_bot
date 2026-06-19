from aiogram import BaseMiddleware
from typing import Any, Callable, Awaitable
from services.user_service import UserService
from services.task_service import TaskService
from database.repositories.tasks_repository import TaskRepository
from database.repositories.user_repository import UserRepository
from psycopg import AsyncConnection

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

        return await handler(event, data)
