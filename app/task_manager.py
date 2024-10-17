
from storage import Storage
from models import Task
from schemas import CreateTask
from typing import Union


class TaskManager:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_task(self, task: CreateTask) -> None:
        self.storage.add(task)

    def delete_task(self, id: Union[int, str]) -> None:
        self.storage.delete(id)

    def update_task(self, id: Union[int, str], name: str, status: str) -> None:
        self.storage.update(id, name, status)

    def task_list(self) -> list[Task]:
        tasks = self.storage.get_list()
        return tasks
