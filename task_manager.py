from task_storage_to_json import Task
from storage import Storage


class TaskManager:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_task(self, name: str) -> None:
        self.storage.add(name)

    def list_tasks(self) -> list[Task]:
        return self.storage.get_list()

    def delete_task(self, id: int) -> None:
        self.storage.delete(id)

    def update_task(self, id: int, name: str, status: str) -> None:
        self.storage.update(id, name, status)
