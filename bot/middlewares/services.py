from aiogram import BaseMiddleware
from typing import Any, Callable, Awaitable
from services.user_service import UserService

class UserServicesMiddleware(BaseMiddleware):

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def __call__(self,
                handler: Callable[
                        [Any, dict[str, Any]],
                        Awaitable[Any]],
                event: Any,
                data: dict[str, Any]
                ):
        data['user_service'] = self.user_service

        return await handler(event, data)

class TaskServicesMiddleware(BaseMiddleware):

    def __init__(self, task_service: UserService):
        self.task_service = task_service

    async def __call__(self,
                handler: Callable[
                        [Any, dict[str, Any]],
                        Awaitable[Any]],
                event: Any,
                data: dict[str, Any]
                ):
        data['task_service'] = self.task_service

        return await handler(event, data)