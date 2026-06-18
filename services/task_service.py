import logging

from database.repositories.tasks_repository import TaskRepository

logger = logging.getLogger(__name__)

class TaskService:
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        
    async def create_task(self, user_id: int, title: str):
        
        task_id = await self.task_repo.create_task(user_id, title)
        
        logger.info(f"Task {title} has created. Task id - {task_id}")
        
        return task_id
    
    async def get_tasks(self, user_id: int):
        
        tasks = await self.task_repo.get_tasks_by_user(user_id)
        
        logger.info(f"Tasks from user {user_id} - {tasks}")
        
        return tasks
    
    async def delete_task(self, task_id: int):
        
        deleted_rows = await self.task_repo.delete_task(task_id)
        
        if deleted_rows:
            logger.info(f"Task {task_id} has deleted")
            return True
            
        else:
            return False
        
    async def mark_done(self, task_id: int, is_done: bool):
        
        await self.task_repo.mark_done(task_id, is_done)
        
        logger.info(f"Task {task_id} has done")
        
        return True