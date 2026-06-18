from database.connection import pool

class TaskRepository:
    
    async def create_task(self, user_id: int, title: str) -> None:
        
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                        INSERT INTO tasks (user_id, title)
                        VALUES (%s, %s)
                        RETURNING id;
                    """,
                    params=(user_id, title,)
                )
                row = await cursor.fetchone()

                return row[0] if row else None
                
    async def get_tasks_by_user(self, user_id: int) -> tuple:
        
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                        SELECT *
                        FROM tasks
                        WHERE user_id = %s;
                    """,
                    params=(user_id, )
                )
                
                row = await cursor.fetchall()
                
        return row
    
    async def delete_task(self, task_id: int) -> int:
        
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                        DELETE FROM tasks
                        WHERE id = %s;
                    """,
                    params=(task_id, )
                )
                
                deleted_rows = cursor.rowcount
                
        return deleted_rows
    
    async def mark_done(self, task_id: int, is_done: bool):
        
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                        UPDATE tasks
                        SET is_done = %s
                        WHERE id = %s
                        ;
                    """,
                    params=(is_done, task_id,)
                )
                   