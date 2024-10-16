from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str 
    


class CreateTask(BaseModel):
    name: str
    

