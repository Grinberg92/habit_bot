from database.models.tasks import Task
from psycopg import AsyncConnection


class TaskRepository:

    def __init__(self, conn: AsyncConnection):
        self.conn = conn
    
    async def create_task(self, user_id: int, title: str) -> Task:
        
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                    INSERT INTO tasks (user_id, title)
                    VALUES (%s, %s)
                    RETURNING *;
                """,
                params=(user_id, title,)
            )
            row = await cursor.fetchone()

            return Task.from_row(row) if row else None
                
    async def get_tasks_by_user(self, user_id: int) -> tuple[Task]:
        
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                    SELECT *
                    FROM tasks
                    WHERE user_id = %s;
                """,
                params=(user_id, )
            )
            
            rows = await cursor.fetchall()
            
            return tuple(Task.from_row(row) for row in rows)
    
    async def get_task_by_id(self, task_id: int) -> Task:

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                        SELECT *
                        FROM tasks
                        WHERE id = %s;
                    """,
                    params=(task_id,)
            )
            row = await cursor.fetchone()

            return Task.from_row(row) if row else None
    
    async def delete_task(self, task_id: int) -> int:
        
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                    DELETE FROM tasks
                    WHERE id = %s;
                """,
                params=(task_id, )
            )
            
            deleted_rows = cursor.rowcount
            
            return deleted_rows
    
    async def mark_done(self, task_id: int, is_done: bool) -> None:
        
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                query="""
                    UPDATE tasks
                    SET is_done = %s
                    WHERE id = %s
                    ;
                """,
                params=(is_done, task_id,)
            )
                