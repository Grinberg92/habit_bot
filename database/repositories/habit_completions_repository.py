from psycopg import AsyncConnection
from database.models.habit_completions import HabitCompletion

class HabitCompletionRepository:

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def done_habit(self, habit_id: int) -> HabitCompletion:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        INSERT INTO habit_completions (habit_id)
                        VALUES (%s)
                        RETURNING *;
                """,
                params=(habit_id,)
            )  
            row = await cursor.fetchone()

            return HabitCompletion.from_row(row=row) if row else None