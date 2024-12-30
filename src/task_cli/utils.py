import json
from enum import Enum
from datetime import datetime
from typing import Any, TypeVar, get_type_hints, get_origin, get_args
from dataclasses import is_dataclass, asdict, fields
from functools import singledispatch

T = TypeVar("T")


@singledispatch
def encode(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)

    return value


@singledispatch
def decode(into: type[T], value: Any) -> T:
    if get_origin(into) is list:
        elem_type = get_args(into)[0]

        if is_dataclass(elem_type):
            return [elem_type.from_dict(item) for item in value]

    return into(value)


@encode.register(datetime)
def _(value: datetime) -> str:
    return value.isoformat()


@encode.register(Enum)
def _(value: Enum) -> str:
    return value.value


@decode.register(datetime)
def _(into, value):
    return into.fromisoformat(value)


def serialize(value: Any) -> str:
    return json.dumps(value, default=encode, indent=4)


def deserialize(into: type[T], data: bytes) -> T:
    deserialized = json.loads(data)
    init_fields = {f.name for f in fields(into) if f.init}
    non_init_fields = {f.name for f in fields(into) if not f.init}

    for key, value in get_type_hints(into).items():
        if key in deserialized:
            deserialized[key] = decode(value, deserialized[key])

    init_values = {k: v for k, v in deserialized.items() if k in init_fields}
    instance = into(**init_values)

    for key in non_init_fields:
        if key in deserialized:
            setattr(instance, key, deserialized[key])

    return instance
