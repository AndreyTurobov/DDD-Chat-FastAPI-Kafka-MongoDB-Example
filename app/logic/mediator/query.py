from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from logic.queries.base import QT, BaseQueryHandler, QR, BaseQuery


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
