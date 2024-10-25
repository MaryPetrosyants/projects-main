
from fastapi import APIRouter
from schemas.schemas import CreateTask
from services.task_manager import TaskManager
from repositories.sqllite_storage import SqlliteStorage
from repositories.json_storage import JsonStorage
from typing import Union
from repositories.auth import get_current_user
from fastapi import Header
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)
# storage = JsonStorage("tasks.json")
storage = SqlliteStorage
manager = TaskManager(storage)


@router.post("/add")
def add(task: CreateTask, Authorization: str = Header(), Refresh_Token: str=Header()):
    current_user = get_current_user(Authorization, Refresh_Token)
    
    manager.add_task(task=task, current_user= current_user )
    return {"message": "Task add"}


@router.delete("/delete")
def delete(id: Union[int, str], Authorization: str = Header(), Refresh_Token: str=Header()):
    current_user = get_current_user(Authorization, Refresh_Token)
    manager.delete_task(id=id, current_user=current_user)
    return {"message": "Task delete"}


@router.put("/update")
def update(id: str, name: str, status: str, Authorization: str = Header(), Refresh_Token: str=Header()):
    current_user = get_current_user(Authorization, Refresh_Token)
    manager.update_task(id=id, name=name, status=status, current_user=current_user)
    return {"message": "Task update"}


@router.get("/task_list")

def get_list(  Refresh_Token: str=Header(),Authorization: str = Header()):
    
    current_user = get_current_user(Authorization, Refresh_Token)
    task_list = manager.task_list(current_user=current_user)
    return task_list
