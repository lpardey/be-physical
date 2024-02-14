from enum import Enum
from typing import TypeVar

T = TypeVar("T")


def get_choices(enumeration: type[Enum], _: type[T]) -> list[tuple[T, str]]:
    return [(e.value, e.name.replace("_", " ").title()) for e in enumeration]
