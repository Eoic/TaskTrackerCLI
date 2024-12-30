from enum import Enum
from typing import Union
from datetime import datetime
from dataclasses import dataclass, field, fields
from task_cli.validator import is_valid_description
from task_cli.utils import serialize


class Status(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'


@dataclass(unsafe_hash=True)
class Task:
    id: int = field(init=False, default=None)
    status: Status
    description: str = field(default='')
    created_at: datetime = field(init=False, default=datetime.now())
    updated_at: Union[datetime, None] = field(init=False, default=None)

    def __post_init__(self):
        if not is_valid_description(self.description):
            raise ValueError('Invalid description.')

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(
            status=Status(data['status']),
            description=data['description'],
        )

        task.id = data['id']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.updated_at = (
            datetime.fromisoformat(data['updated_at']) if data['updated_at'] else None
        )

        return task

    def __str__(self):
        text = '=' * 80
        text += '\n| ID:'.ljust(16) + f'{self.id}'
        text += '\n| Status:'.ljust(
            16
        ) + f'{self.status.value.upper().replace('_', ' ')}'.ljust(15)
        text += '\n| Description:'.ljust(16) + f'{self.description}'.ljust(15)
        text += '\n| Created at:'.ljust(
            16
        ) + f'{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}'.ljust(15)
        text += '\n| Updated at:'.ljust(
            16
        ) + f'{self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at is not None else 'Never'}'.ljust(
            15
        )
        text += '\n' + '=' * 80

        return text


@dataclass
class TaskDocument:
    next_id: int = 1
    tasks: list[Task] = field(default_factory=list)

    def find_one(self, data: dict) -> Union[Task, None]:
        for task in self.tasks:
            if all(getattr(task, key) == value for key, value in data.items()):
                return task

        return None

    def find_all(self, data: dict) -> list[Task]:
        tasks = []

        for task in self.tasks:
            if all(getattr(task, key) == value for key, value in data.items()):
                tasks.append(task)

        return tasks

    def add(self, task: Task):
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1

    def add_many(self, *tasks: Task):
        for task in tasks:
            self.add(task)

    def update(self, task: Task, data: dict):
        try:
            task_index = self.tasks.index(task)
        except ValueError:
            return False

        init_fields = {f.name for f in fields(Task) if f.init}

        for key, value in data.items():
            if key in init_fields:
                setattr(task, key, value)

        task.updated_at = datetime.now()
        self.tasks[task_index] = task

        return True

    def delete(self, data: dict) -> bool:
        tasks = self.find_all(data)

        for task in tasks:
            self.tasks.remove(task)

        return len(tasks) > 0

    def __str__(self):
        return f'[{self.__class__.__name__}]\n{serialize(self)}'
