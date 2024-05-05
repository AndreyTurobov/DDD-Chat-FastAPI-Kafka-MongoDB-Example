from dataclasses import dataclass

from domain.exceptions.messages import (
    EmptyTextException,
    TitleTooLongException,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    def validate(self) -> None:
        min_length: int = 3
        max_length: int = 255

        if not self.value:
            raise EmptyTextException()

        if min_length > len(self.value) > max_length:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
