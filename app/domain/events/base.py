from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID

from uuid_extensions import uuid7


@dataclass
class BaseEvent(ABC):
    event_id: UUID = field(
        default_factory=uuid7,
        kw_only=True,
    )
