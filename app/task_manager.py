
from storage import Storage
from fastapi import APIRouter, Depends
from models import Task
from database import get_db
from sqlalchemy.orm import Session
from schemas import CreateTask


class TaskManager:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def add_task(self, task:CreateTask) -> None:
        self.storage.add(task)

    def delete_task(self, id:int) -> None:
        self.storage.delete(id)

    def update_task(self, id: int, name: str, status: str) -> None:
        self.storage.update(id, name, status)
        

    def task_list(self)-> list[Task]:
        tasks = self.storage.get_list()
        return tasks
