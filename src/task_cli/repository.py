from typing import List, Union
from task_cli.database import Database
from task_cli.model import Status, Task


class TaskRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_by_id(self, id: int) -> Union[Task, None]:
        return self.db.document.find_one({'id': id})

    def find_by_status(self, status: List[Status] = None) -> List[Task]:
        if status is None:
            status = [Status.TODO, Status.IN_PROGRESS, Status.DONE]

        tasks = set()

        for s in status:
            tasks.update(self.db.document.find_all({'status': s}))

        return list(tasks)

    def add(self, task: Task):
        self.db.document.add(task)
        self.db.commit()

    def update(self, task: Task, data: dict):
        is_updated = self.db.document.update(task, data)
        self.db.commit()
        return is_updated

    def delete_by_id(self, id: int) -> bool:
        is_deleted = self.db.document.delete({'id': id})
        self.db.commit()
        return is_deleted

    def size(self) -> int:
        return len(self.db.document.tasks)
