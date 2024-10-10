from task_storage_to_json import Task
from typing import Any
from storage import Storage
import uuid

class TaskManager:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_task(self, task_name) -> str:
        task_id = uuid.uuid4()
        new_task = Task(int(task_id), task_name)
        return self.storage.add(new_task)

    def list_tasks(self) -> list[Task]:
        return self.storage.get_list()

    def delete_task(self, task_id) -> str:
        return self.storage.delete(task_id)
