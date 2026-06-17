from database.repositories.tasks_repository import TaskRepository

class TaskService:
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        
    def create_task(self, user_id: int, title: str):
        
        new_task = self.task_repo.create_task(user_id, title)
        
        print(f"Task {title} has created")
        
        return new_task
    
    def get_tasks(self, user_id: int):
        
        tasks = self.task_repo.get_tasks_by_user(user_id)
        
        print(f"Tasks from user {user_id} - {tasks}")
        
        return tasks
    
    def delete_task(self, task_id: int):
        
        deleted_rows = self.task_repo.delete_task(task_id)
        
        if deleted_rows:
            print(f"Task {task_id} has deleted")
            return True
            
        else:
            return False
        
    def mark_done(self, task_id: int, is_done: bool):
        
        self.task_repo.mark_done(task_id, is_done)
        
        print(f"Task {task_id} has done")
        
        return True