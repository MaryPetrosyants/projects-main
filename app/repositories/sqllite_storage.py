from models.models import Task
from exceptions.task_exception import TaskError, TaskNotFound, TaskAlreadyExistError
from repositories.storage import Storage
from schemas.schemas import CreateTask
from config.database import get_db
from repositories.auth import get_current_user
from typing import Annotated
from fastapi import Depends
from schemas.user import CreateUser, UserSchema, CurrentUser
class SqlliteStorage(Storage):

    def add(task: CreateTask, current_user) -> None:
        user_id=current_user.id
        db = next(get_db())
        db_task = Task(name=task.name, user_id=user_id)
        db.add(db_task)
        db.commit()

    def delete(id: int, current_user) -> None:
        user_id=current_user.id
        
        db = next(get_db())
        db_task = db.query(Task).filter(Task.id == id).first()
        if user_id == db_task.user_id:
            db.delete(db_task)
            db.commit()
        

    def update(id: int, name: str, status: str, current_user) -> None:
        db = next(get_db())
        user_id=current_user.id
        task = db.query(Task).filter(Task.id == id).first()
        if task:
            if user_id == task.user_id:
                task.name = name
                task.id = id
                task.status = status
                db.commit()

        else:
            raise TaskNotFound(id)

    def get_list(current_user) -> list[Task]:
        db = next(get_db())
        user_id=current_user.id
        return db.query(Task).filter(Task.user_id == user_id).all()
