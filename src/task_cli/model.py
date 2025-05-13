from enum import Enum
from typing import Union
from datetime import datetime, date
from dataclasses import dataclass, field, fields, MISSING
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
    due_date: date | None = None
    updated_at: datetime = field(default_factory=datetime.now)
    _dirty_fields: set[str] = field(init=False, default_factory=set, repr=False)

    def __init__(self, **kwargs):
        self._dirty_fields = set(kwargs.keys())

        for obj_field in fields(self):
            if obj_field.name == "_dirty_fields":
                continue

            if obj_field.name in kwargs:
                value = kwargs[obj_field.name]
            elif obj_field.default_factory is not MISSING:
                value = obj_field.default_factory()
            elif obj_field.default is not MISSING:
                value = obj_field.default
            else:
                value = None

            setattr(self, obj_field.name, value)

        self._dirty_fields.add("updated_at")

    def __post_init__(self):
        if self.description is not None and not is_valid_description(self.description):
            raise ValueError("Invalid description.")

    def items(self):
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if field.name != "_dirty_fields"
        }.items()

    def is_set(self, field_name: str) -> bool:
        return field_name in self._dirty_fields


@dataclass(unsafe_hash=True)
class Task:
    id: int
    status: Status
    description: str
    due_date: date | None
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
        text += "\n| Due date:".ljust(16) + f"{self.due_date}".ljust(15)
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
