import json
from datetime import datetime
from typing import Any, TypeVar, get_type_hints
from dataclasses import is_dataclass, asdict
from functools import singledispatch

T = TypeVar("T")


@singledispatch
def encode(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)

    return value


@singledispatch
def decode(into: type[T], value: Any) -> T:
    return into(value)


@encode.register(datetime)
def _(value: datetime) -> str:
    return value.isoformat()


@decode.register(datetime)
def _(into, value):
    return into.fromisoformat(value)


def serialize(value: Any) -> str:
    return json.dumps(value, default=encode, indent=4)


def deserialize(into: type[T], data: bytes) -> T:
    deserialized = json.loads(data)

    for key, value in get_type_hints(into).items():
        if key in deserialized:
            deserialized[key] = decode(value, deserialized[key])

    return into(**deserialized)
