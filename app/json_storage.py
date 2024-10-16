import json
import os
from typing import Any
import uuid
from storage import Storage
from dataclasses import asdict
from models import Task, TaskJson
from schemas import CreateTask, TaskSchema
from fastapi.encoders import jsonable_encoder
from task_exception import TaskError, TaskNotFound, TaskAlreadyExistError


class JsonStorage(Storage):

    def __init__(self, filename) -> None:
        self.filename = filename

    def load_tasks(self) -> list[Task]:
        if os.path.exists(self.filename):

            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
            return [Task(**task) for task in tasks_data]

    def add(self, task: TaskJson) -> None:
        dbtask = TaskJson(
            name=task.name,
            id=str(uuid.uuid4())

        )
        self.update(dbtask)

    def delete(self, task_id) -> None:
        tasks = self.load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        self.update(tasks)

    def update(self, id:str, name=None, status=None) -> None:
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == id:
                if name is not None:
                    task.name = name
                if status is not None:
                    task.status = status
                break
        else: raise TaskNotFound(id)
        self.save(tasks)

        # with open(self.filename, 'w') as file:
        #     json.dump([jsonable_encoder(task)
        #               for task in tasks], file, indent=4)

    def save(self, tasks):
        with open(self.filename, 'w') as file:
            json.dump(jsonable_encoder(tasks), file, indent=4)


    def get_list(self) -> list[Task]:
        return self.load_tasks()
