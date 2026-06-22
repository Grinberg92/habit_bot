from database.models.user import User
from psycopg import AsyncConnection

class UserRepository:

    def __init__(self, conn: AsyncConnection):
          self.conn = conn

    async def create_user(self, telegram_id: int, username: str) -> User:

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""INSERT INTO users (telegram_id, username)
                        VALUES(%s, %s)
                        RETURNING *;
                
                """,
                params=(telegram_id, username,)
            )
            row = await cursor.fetchone()

            return User.from_row(row)

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""SELECT *
                        FROM users
                        WHERE telegram_id = %s;
                """,
                params=(telegram_id,)
            )
            row = await cursor.fetchone()

            return User.from_row(row)
    
    async def delete_user_by_telegram_id(self, telegram_id: int) -> int:

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""DELETE FROM users
                        WHERE telegram_id = %s;
                
                """,
                params=(telegram_id,)
            )
            
            deleted_rows = cursor.rowcount
            
            return deleted_rows

    async def update_username_by_telegram_id(self, telegram_id: int, username: str) -> None:

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE users
                SET username = %s
                WHERE telegram_id = %s
                """,
                params=(username, telegram_id,)
            )

