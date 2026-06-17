from database.connection import pool

class UserRepository:
    def create_user(self, telegram_id: int, username: str):

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""INSERT INTO users (telegram_id, username)
                            VALUES(%s, %s);
                    
                    """,
                    params=(telegram_id, username,)
                )

    def get_user_by_telegram_id(self, telegram_id: int):

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""SELECT *
                            FROM users
                            WHERE telegram_id = %s;
                    
                    """,
                    params=(telegram_id,)
                )
                row = cursor.fetchone()

        return row
    
    def delete_user_by_telegram_id(self, telegram_id: int):

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""DELETE FROM users
                            WHERE telegram_id = %s;
                    
                    """,
                    params=(telegram_id,)
                )
                
                deleted_rows = cursor.rowcount
                
        return deleted_rows

    def update_username_by_telegram_id(self, telegram_id: int, username: str):

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET username = %s
                    WHERE telegram_id = %s
                    """,
                    params=(username, telegram_id,)
                )

