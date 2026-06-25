from psycopg import AsyncConnection
from database.models.habits import Habit

class HabitRepository:

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create_habit(self, user_id: int, title: str, reminder_time: str) -> Habit:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        INSERT INTO habits (user_id, title, reminder_time)
                        VALUES (%s, %s, %s)
                        RETURNING *;
                """,
                params=(user_id, title, reminder_time,)
            )
            row = await cursor.fetchone()

            return Habit.from_row(row=row) if row else None

    async def get_habits_by_user(self, user_id: int) -> tuple[Habit]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        SELECT *
                        FROM habits
                        WHERE user_id = %s;
                """,
                params=(user_id,)
            )
            rows = await cursor.fetchall()

            return tuple(Habit.from_row(row=row) for row in rows)

    async def get_habit_by_id(self, habit_id: int) -> Habit | None:

        async with self.conn.cursor() as cursor:

            await cursor.execute(
                """
                SELECT *
                FROM habits
                WHERE id = %s;
                """,
                (habit_id,)
            )

            row = await cursor.fetchone()

            return Habit.from_row(row) if row else None
        
    async def get_active_habits(self) -> tuple[Habit]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        SELECT *
                        FROM habits
                        WHERE is_active = true;
                """
            )
            rows = await cursor.fetchall()

            return tuple(Habit.from_row(row=row) for row in rows)

    async def set_active_habit(self, habit_id: int, is_active: bool) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        UPDATE habits
                        SET is_active = %s
                        WHERE id = %s;
                """,
                params=(is_active, habit_id,)
            )

            return cursor.rowcount
        
    async def delete_habit(self, habit_id: int) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        DELETE FROM habits
                        WHERE id = %s;
                """,
                params=(habit_id,)
            )
            
            delete_rows = cursor.rowcount

            return delete_rows
        
    async def update_habit_title(self, habit_id: int, title: str) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        UPDATE habits
                        SET title = %s
                        WHERE id = %s;
                """,
                params=(title, habit_id,)
            )

            return cursor.rowcount
        
    async def update_habit_time(self, habit_id: int, time: str) -> int:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        UPDATE habits
                        SET reminder_time = %s
                        WHERE id = %s;
                """,
                params=(time, habit_id,)
            )

            return cursor.rowcount
        
        