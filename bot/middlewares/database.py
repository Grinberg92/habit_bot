from aiogram import BaseMiddleware
from typing import Any, Callable, Awaitable
from database.connection import pool

class DatabaseMiddleware(BaseMiddleware):

    async def __call__(self,
                handler: Callable[
                        [Any, dict[str, Any]],
                        Awaitable[Any]],
                event: Any,
                data: dict[str, Any]
                ):
        
        async with pool.connection() as conn:

            data['conn'] = conn

            return await handler(event, data)
