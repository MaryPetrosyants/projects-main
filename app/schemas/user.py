from typing import List
from pydantic import BaseModel, Field, ConfigDict


class UserSchema(BaseModel):
    id : int
    name: str
    email: str
    password: str


class CreateUser(BaseModel):
    name: str
    email: str
    password: str

class UserInDB(UserSchema):
    hashed_password: str

class CurrentUser(BaseModel):
    id: int
