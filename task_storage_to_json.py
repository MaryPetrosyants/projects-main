import json
import os
from typing import Any
from storage import Storage
from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    name: str
    status: str = "Not done"


class TaskStorageToJson(Storage):

    def __init__(self, filename) -> None:
        self.filename = filename

    def load_tasks(self) -> list[Task]:
        if os.path.exists(self.filename):

            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
            return [Task(**task) for task in tasks_data]

    def save(self, tasks: list[Task]) -> str:
        with open(self.filename, 'w') as file:
            json.dump([asdict(task) for task in tasks], file, indent=4)
        return "Task update"

    def add(self, task: Task) -> str:
        tasks = self.load_tasks()
        tasks.append(task)
        return self.save(tasks)

    def delete(self, task_id) -> str:
        tasks = self.load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        return self.save(tasks)

    def update(self):
        pass

    def get_list(self) -> list[Task]:
        return self.load_tasks()
