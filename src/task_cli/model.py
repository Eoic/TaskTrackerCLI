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

            value = None

            if obj_field.name in kwargs:
                value = kwargs[obj_field.name]
            elif obj_field.default_factory is not MISSING:
                value = obj_field.default_factory()
            elif obj_field.default is not MISSING:
                value = obj_field.default

            setattr(self, obj_field.name, value)

        self._dirty_fields.add("updated_at")
        self.__post_init__()

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
        rows = []
        max_title_len = 0
        max_value_len = 0
        title_padding = 1
        value_padding = 1
        extra_symbols = 5

        for obj_field in fields(self):
            value = getattr(self, obj_field.name)
            value_repr = "-"

            if isinstance(value, datetime):
                value_repr = value.strftime("%Y-%m-%d %H:%M:%S")
            elif value is None:
                value_repr = "-"
            else:
                value_repr = str(value)

            max_title_len = max(max_title_len, len(obj_field.name))
            max_value_len = max(max_value_len, len(value_repr))

            rows.append(
                (
                    obj_field.name.upper(),
                    value_repr,
                )
            )

        border_width = (
            max_title_len
            + title_padding
            + max_value_len
            + value_padding
            + extra_symbols
        )

        text = "-" * border_width

        for title, value in rows:
            text += (
                "\n| "
                + title.ljust(max_title_len + title_padding)
                + "| "
                + value.ljust(max_value_len + value_padding)
                + "|"
            )

        text += "\n"
        text += "-" * border_width

        return text
