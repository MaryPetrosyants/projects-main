
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from schemas import CreateTask
from task_manager import TaskManager
from sqllite_storage import SqlliteStorage
from json_storage import JsonStorage

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)
storage = JsonStorage("tasks.json")
#storage = SqlliteStorage
manager = TaskManager(storage)


@router.post("")
def add(task:CreateTask= Depends()):
    manager.add_task(task=task )
    return {"message": "Task add" }


@router.delete("")
def delete(id:str):
    manager.delete_task(id=id)
    return {"message": "Task delete" }
    


@router.put("")
def update(id: str, name: str, status: str):
    manager.update_task(id=id,name=name,status=status)
    return {"message": "Task update"}


@router.get("")
def get_list():
    task_list = manager.task_list()
    return task_list
