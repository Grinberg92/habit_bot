from database.repositories.user_repository import UserRepository

class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    def register_user(self, telegram_id: int, username: str):
        user = self.user_repo.get_user_by_telegram_id(telegram_id)
        
        if user:
            print(f"User {user[2]} already exist")
            return False
        
        self.user_repo.create_user(telegram_id, username)
        
        print(f"User {username} has created")
        
        return True
    
    def change_username(self, telegram_id: int, username: str):
        
        self.user_repo.update_username_by_telegram_id(telegram_id, username)
        
        print(F"User {telegram_id} has updated")
        
        return True
    
    def delete_user(self, telegram_id: int):
        
        deleted_row = self.user_repo.delete_user_by_telegram_id(telegram_id)
        
        if deleted_row:
            print(F"User {telegram_id} has deleted")
            
        else:
            print(deleted_row)
        
        return True