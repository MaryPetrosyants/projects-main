import json
import os
from typing import Any
import uuid
from storage import Storage
from dataclasses import asdict
from task import Task


class TaskStorageToJson(Storage):

    def __init__(self, filename) -> None:
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self

    def load_tasks(self) -> list[Task]:
        if os.path.exists(self.filename):

            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
            return [Task(**task) for task in tasks_data]

    def add(self, name) -> None:
        task = Task(
            name=name,
            id=str(uuid.uuid4())
        )
        self.update(task)

    def delete(self, task_id) -> None:
        tasks = self.load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        self.save(tasks)

    def update(self, task: Task):
        tasks = self.load_tasks()
        tasks.append(task)
        with open(self.filename, 'w') as file:
            json.dump([asdict(task) for task in tasks], file, indent=4)

    def get_list(self) -> list[Task]:
        return self.load_tasks()
