import logging
from database.repositories.user_repository import UserRepository
from database.models.user import User

logger = logging.getLogger(__name__)

class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    async def register_user(self, telegram_id: int, username: str) -> User:
        user= await self.user_repo.get_user_by_telegram_id(telegram_id)
        
        if user:
            logger.info(f"User {user.username} already exist")
            return False
        
        reg_user = await self.user_repo.create_user(telegram_id, username)
        
        logger.info(f"User {username} has created")
        
        return reg_user
    
    async def change_username(self, telegram_id: int, username: str) -> bool:
        
        await self.user_repo.update_username_by_telegram_id(telegram_id, username)
        
        logger.info(F"User {telegram_id} has updated")
        
        return True
    
    async def delete_user(self, telegram_id: int) -> bool:
        
        deleted_row = await self.user_repo.delete_user_by_telegram_id(telegram_id)
        
        if deleted_row:
            logger.info(F"User {telegram_id} has deleted")
            
        else:
            logger.info(deleted_row)
        
        return True