import sqlite3
from sqlite3 import Error
from storage import Storage
from storage_to_db import StorageToDb
from task import Task
from task_exception import TaskError, TaskNotFound, TaskAlreadyExistError


class StorageToSqllite(Storage, StorageToDb):

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def create_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'Not done'
            )
            ''')
        self.connection.commit

    def add(self, name: str) -> None:

        if self.get_item_by_name(name) is None:
            self.cursor.execute(
                'INSERT INTO Tasks (name) VALUES (?)', (name,))
            self.connection.commit()
        else:
            raise TaskAlreadyExistError(name)

    def delete(self, id: int) -> None:
        if self.get_item_by_id(id) is not None:
            self.cursor.execute('DELETE FROM Tasks WHERE id = ?', (id,))
            self.connection.commit()
        else:
            raise TaskNotFound(id)

    def update(self, id: int, name: str, status: str) -> None:
        if self.get_item_by_id(id) is not None:
            self.cursor.execute(
                'UPDATE Tasks SET name = ? status = ? WHERE id = ?', (name, status, id))
            self.connection.commit()
        else:
            raise TaskNotFound(id)

    def get_list(self) -> list[Task]:
        self.cursor.execute('SELECT * FROM Tasks')
        tasks = self.cursor.fetchall()
        return [Task(*task)for task in tasks]

    def get_item_by_name(self, name: str) -> Task:
        self.cursor.execute('SELECT * FROM Tasks WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        return Task(*row) if row else None

    def get_item_by_id(self, id: int) -> Task:
        self.cursor.execute('SELECT * FROM Tasks WHERE id = ?', (id,))
        row = self.cursor.fetchone()
        return Task(*row) if row else None
