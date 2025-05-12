import json
from typing import Any
from dataclasses import is_dataclass, asdict
from functools import singledispatch


@singledispatch
def encode(value: Any) -> Any:
    if is_dataclass(value):
        if not isinstance(value, type):
            return asdict(value)

    return value


def serialize(value: Any) -> str:
    return json.dumps(value, default=encode, indent=4)
