from database.connection import pool
from database.repositories.user_repository import UserRepository

def main():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT version();')
            print(f"🔍 autocommit = {conn.autocommit}") 
            version = cur.fetchone()

            print(version)

    conn.close()

def main2():
    # UserRepository().create_user('55555', 'sveta')
    # UserRepository().delete_user_by_telegram_id('55555')
    # UserRepository().get_user_by_telegram_id('11111')
    UserRepository().update_username_by_telegram_id('4444', 'sasha')

if __name__ == '__main__':
    main2() 