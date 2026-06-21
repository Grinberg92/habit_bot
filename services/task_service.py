import logging

from database.repositories.tasks_repository import TaskRepository
from database.models.tasks import Task

logger = logging.getLogger(__name__)

class TaskService:
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        
    async def create_task(self, user_id: int, title: str) -> Task:
        
        task = await self.task_repo.create_task(user_id, title)

        
        logger.info(f"Task {title} has created. Task id - {task.id}")
        return task
    
    async def get_tasks_by_user(self, user_id: int, page: int = 1, limit: int = 5) -> tuple[Task]:

        offset = (page - 1) * limit
        
        tasks= await self.task_repo.get_tasks_by_user(user_id=user_id, limit=limit, offset=offset)
        
        logger.info(f"Tasks from user {user_id} - {tasks}")
        
        return tasks
    
    async def get_task_by_id(self, task_id: int):

        task = await self.task_repo.get_task_by_id(task_id)

        logger.info(f"Task {task.id}")  

        return task      
    
    async def delete_task(self, task_id: int) -> bool:
        
        deleted_rows = await self.task_repo.delete_task(task_id)
        
        if deleted_rows:
            logger.info(f"Task {task_id} has deleted")
            return True
            
        else:
            return False
        
    async def mark_done(self, task_id: int, is_done: bool) -> bool:
        
        await self.task_repo.mark_done(task_id, is_done)
        
        logger.info(f"Task {task_id} has done")
        
        return True