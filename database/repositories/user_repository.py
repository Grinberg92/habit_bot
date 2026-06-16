from database.connection import pool

class UserRepository:
    def create_user(self, telegram_id: int, username: str):
        user = self.get_user_by_telegram_id(telegram_id)

        if user:
            print(f"Already exist")
            return 
        
        pool.open()

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""INSERT INTO users (telegram_id, username)
                            VALUES(%s, %s);
                    
                    """,
                    params=(telegram_id, username,)
                )
                print(f"Add user {username}")


    def get_user_by_telegram_id(self, telegram_id: int):

        pool.open()

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

                if row is not None:
                    print(f"Get user {row}")
        return row
    
    def delete_user_by_telegram_id(self, telegram_id: int):

        pool.open()

        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query="""DELETE FROM users
                            WHERE telegram_id = %s;
                    
                    """,
                    params=(telegram_id,)
                )

    def update_username_by_telegram_id(self, telegram_id: int, username: str):

        pool.open()

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
                print(f"User {telegram_id} has updated name {username}")
