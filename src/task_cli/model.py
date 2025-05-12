from enum import Enum
from typing import Union
from datetime import datetime
from dataclasses import dataclass
from task_cli.validator import is_valid_description


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@dataclass
class CreateTask:
    status: Status
    description: str

    def __post_init__(self):
        if not is_valid_description(self.description):
            raise ValueError("Invalid description.")


@dataclass
class UpdateTask:
    status: Status | None = None
    description: str | None = None

    def __post_init__(self):
        if self.description is not None and not is_valid_description(self.description):
            raise ValueError("Invalid description.")


@dataclass(unsafe_hash=True)
class Task:
    id: int
    status: Status
    description: str
    created_at: datetime
    updated_at: Union[datetime, None]

    def __post_init__(self):
        if not is_valid_description(self.description):
            raise ValueError("Invalid description.")

    def __str__(self):
        text = "-" * 80
        text += "\n| ID:".ljust(16) + f"{self.id}"
        text += "\n| Status:".ljust(
            16
        ) + f"{self.status.value.upper().replace('_', ' ')}".ljust(15)
        text += "\n| Description:".ljust(16) + f"{self.description}".ljust(15)
        text += "\n| Created at:".ljust(
            16
        ) + f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}".ljust(15)
        text += (
            "\n| Updated at:".ljust(16)
            + f"{self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at is not None else 'Never'}".ljust(
                15
            )
        )
        text += "\n" + "-" * 80

        return text
