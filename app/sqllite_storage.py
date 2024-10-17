from models import Task
from task_exception import TaskError, TaskNotFound, TaskAlreadyExistError
from storage import Storage
from schemas import CreateTask
from database import get_db


class SqlliteStorage(Storage):

    def add(task: CreateTask) -> None:
        db = next(get_db())
        db_task = Task(name=task.name)
        db.add(db_task)
        db.commit()

    def delete(id: int) -> None:
        db = next(get_db())
        db_task = db.query(Task).filter(Task.id == id).first()
        db.delete(db_task)
        db.commit()

    def update(id: int, name: str, status: str) -> None:
        db = next(get_db())
        task = db.query(Task).filter(Task.id == id).first()
        if task:
            task.name = name
            task.id = id
            task.status = status
            db.commit()

        else:
            raise TaskNotFound(id)

    def get_list() -> list[Task]:
        db = next(get_db())
        return db.query(Task).all()
