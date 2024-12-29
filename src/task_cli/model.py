from enum import Enum
from typing import Union
from itertools import count
from datetime import datetime
from dataclasses import dataclass, field

from task_cli.utils import serialize


class Status(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'


@dataclass
class Task:
    id: int = field(init=False, default=None)
    status: Status
    description: str
    created_at: datetime = field(init=False, default=datetime.now())
    updated_at: Union[datetime, None] = field(init=False, default=None)


@dataclass
class TaskDocument:
    next_id: int = 1
    tasks: list[Task] = field(default_factory=list)

    def get(self, id: int) -> Union[Task, None]:
        for task in self.tasks:
            if task.id == id:
                return task

        return None

    def add(self, task: Task):
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1

    def bulk_add(self, *tasks: Task):
        for task in tasks:
            self.add(task)

    def update(self, id: int, task: Task):
        if not self.exists(id):
            raise ValueError(f'Task with id {id} does not exist.')

        task.id = id
        task.updated_at = datetime.now()
        self.tasks[self.tasks.index(self.get(id))] = task

    def delete(self, id: int) -> bool:
        try:
            self.tasks.remove(self.get(id))
            return True
        except ValueError:
            return False

    def bulk_delete(self, *ids: int):
        for id in ids:
            self.delete(id)

    def exists(self, id: int) -> bool:
        return self.get(id) is not None

    def __str__(self):
        return f'[{self.__class__.__name__}]\n{serialize(self)}'
