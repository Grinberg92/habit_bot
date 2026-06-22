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

            return Habit.from_row(row=row)

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