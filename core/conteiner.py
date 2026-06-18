from database.repositories.user_repository import UserRepository
from database.repositories.tasks_repository import TaskRepository
from services.user_service import UserService
from services.task_service import TaskService

class Container:

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_service = UserService(user_repo=self.user_repository)

        self.task_repository = TaskRepository()
        self.task_service = TaskService(task_repo=self.task_repository)


container = Container()