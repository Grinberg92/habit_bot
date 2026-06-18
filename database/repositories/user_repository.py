from database.connection import pool

class UserRepository:
    async def create_user(self, telegram_id: int, username: str):

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""INSERT INTO users (telegram_id, username)
                            VALUES(%s, %s);
                    
                    """,
                    params=(telegram_id, username,)
                )

    async def get_user_by_telegram_id(self, telegram_id: int):

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""SELECT *
                            FROM users
                            WHERE telegram_id = %s;
                    
                    """,
                    params=(telegram_id,)
                )
                row = await cursor.fetchone()

        return row
    
    async def delete_user_by_telegram_id(self, telegram_id: int):

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""DELETE FROM users
                            WHERE telegram_id = %s;
                    
                    """,
                    params=(telegram_id,)
                )
                
                deleted_rows = cursor.rowcount
                
        return deleted_rows

    async def update_username_by_telegram_id(self, telegram_id: int, username: str):

        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE users
                    SET username = %s
                    WHERE telegram_id = %s
                    """,
                    params=(username, telegram_id,)
                )

