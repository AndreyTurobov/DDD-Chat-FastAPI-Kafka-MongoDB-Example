from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Couldn't find handlers for event: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Couldn't find handlers for command: {self.command_type}"
