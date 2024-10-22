
from repositories.storage import Storage
from models.models import Task
from schemas.schemas import CreateTask
from typing import Union


class TaskManager:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_task(self, task: CreateTask, current_user) -> None:
        self.storage.add(task, current_user)

    def delete_task(self, id: Union[int, str], current_user) -> None:
        self.storage.delete(id, current_user)

    def update_task(self, id: Union[int, str], name: str, status: str, current_user) -> None:
        self.storage.update(id, name, status, current_user)

    def task_list(self, current_user) -> list[Task]:
        tasks = self.storage.get_list(current_user)
        return tasks
