import json
from typing import Any

class Task:

    def __init__(self, name, id, status):
        self.name = name   
        self.id = id
        self.status = status

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "status":self.status
        }
    
    def __str__(self) -> str:
        return f"{self.id=}, {self.name=}, {self.status=}"
        
 

class TaskManager:
    def __init__(self, filename = 'tasks.json') -> None:
        self.tasks: list[Task] = []
        self.filename: str = filename
        self.load_tasks()

    def to_dict(self) -> dict[str, Any]:
        result = dict()
        for task in self.tasks:
            result[task.id] = task.to_dict()
        return result

    def load_tasks(self) -> None:
        try:
            with open(self.filename, 'r') as file:
                json_data = json.load(file)
                for task_id in json_data:
                    temp_obj = Task(name=json_data[task_id]["name"], id=json_data[task_id]["id"], status=json_data[task_id]["status"] )
                    self.tasks.append(temp_obj)
                if not self.tasks:
                    raise Exception("File is empty")
        except FileNotFoundError:
            print(f"Not found {self.filename }")

    def save_tasks(self) -> None:
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.to_dict(), file)
        except FileNotFoundError:
            print(f"Not found {self.filename }")
        except Exception as e:
            print(f"Error {e}")
    
    def add_task(self, name) -> Task:
        try:
            if not name:
                raise Exception("Not name task")
            task_id=len(self.tasks) + 1
            task = Task(name,task_id,status="not done")
            self.tasks.append(task)
            self.save_tasks()
        except Exception as e:
            print(f"Error {e}")
        return task
        

    def list_tasks(self) -> list[Task]:
        list_tasks = []
        for task in self.tasks:
            list_tasks.append(task)
        return list_tasks

    def delete_task(self,task_id) -> str:
        flag_delete = 0
        try:
            for i, task in enumerate(self.tasks):
                if task.id == task_id:
                    del self.tasks[i]
                    flag_delete = 1
                    self.save_tasks()
                    break
                
            if flag_delete == 1: 
                return (f"task {task_id} delete")
            else: 
                raise Exception("Task not found")

        except Exception as e:
            print(f"Error {e}")
        
        
