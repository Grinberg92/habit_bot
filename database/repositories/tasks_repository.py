from database.connection import pool

class TaskRepository:
    
    def create_task(self, user_id: int, title: str) -> None:
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""
                        INSERT INTO tasks (user_id, title)
                        VALUES (%s, %s);
                    """,
                    params=(user_id, title,)
                )
                
    def get_tasks_by_user(self, user_id: int) -> tuple:
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""
                        SELECT *
                        FROM tasks
                        WHERE user_id = %s;
                    """,
                    params=(user_id, )
                )
                
                row = cursor.fetchall()
                
        return row
    
    def delete_task(self, task_id: int) -> int:
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""
                        DELETE FROM tasks
                        WHERE id = %s;
                    """,
                    params=(task_id, )
                )
                
                deleted_rows = cursor.rowcount
                
        return deleted_rows
    
    def mark_done(self, task_id: int, is_done: bool):
        
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""
                        UPDATE tasks
                        SET is_done = %s
                        WHERE id = %s
                        ;
                    """,
                    params=(is_done, task_id,)
                )
                   