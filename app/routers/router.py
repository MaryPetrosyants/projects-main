
from fastapi import APIRouter, Depends
from schemas.schemas import CreateTask
from services.task_manager import TaskManager
from repositories.sqllite_storage import SqlliteStorage
from repositories.json_storage import JsonStorage
from typing import Union
from typing import Annotated
from schemas.user import CreateUser, UserSchema, CurrentUser
from repositories.auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)
# storage = JsonStorage("tasks.json")
storage = SqlliteStorage
manager = TaskManager(storage)


@router.post("")
def add(current_user: Annotated[UserSchema, Depends(get_current_user)],task: CreateTask = Depends()):
    manager.add_task(task=task, current_user=current_user)
    return {"message": "Task add"}


@router.delete("")
def delete(current_user: Annotated[UserSchema, Depends(get_current_user)],id: Union[int, str]):
    manager.delete_task(id=id, current_user=current_user)
    return {"message": "Task delete"}


@router.put("")
def update(current_user: Annotated[UserSchema, Depends(get_current_user)],id: str, name: str, status: str):
    manager.update_task(id=id, name=name, status=status, current_user=current_user)
    return {"message": "Task update"}


@router.get("")
def get_list(current_user: Annotated[UserSchema, Depends(get_current_user)],):
    task_list = manager.task_list(current_user=current_user)
    return task_list
