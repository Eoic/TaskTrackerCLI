from tkinter import N
from typing import List
from task_cli.database import Database
from task_cli.model import Status, Task


class TaskRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, task: Task):
        self.db.document.add(task)
        self.db.commit()

    def update(self, id: int, task: Task):
        self.db.document.update(id, task)
        self.db.commit()

    def delete(self, id: int):
        self.db.document.delete(id)
        self.db.commit()

    def filter(self, status: List[Status] = None) -> List[Task]:
        if status is None:
            status = [Status.TODO, Status.IN_PROGRESS, Status.DONE]

        return [task for task in self.db.document.tasks if task.status in status]
