from abc import ABC
from dataclasses import dataclass, field

from uuid_extensions import uuid7str


@dataclass
class BaseEvent(ABC):
    event_id: str = field(
        default_factory=lambda: uuid7str(),
        kw_only=True,
    )
