class TaskError(Exception):
    pass


class TaskNotFound(TaskError):
    def __init__(self, id: int):
        super().__init__(f"Task {id} not found")


class TaskAlreadyExistError(TaskError):
    def __init__(self, name: str):
        super().__init__(f"Task {name} alredy exists")
