from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=True, default="Not done")
    user_id = Column(Integer, index=True)

class TaskJson(BaseModel):
    id: str
    name: str
    status: str = "Not done"


