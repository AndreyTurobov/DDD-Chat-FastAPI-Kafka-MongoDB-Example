from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"Chat with that title already exists: {self.title}"
