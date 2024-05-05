from pydantic.main import BaseModel

from infra.repositories.filters.messages import (
    GetAllChatsFilters as GetAllChatsInfraFilters,
)
from infra.repositories.filters.messages import (
    GetMessagesFilters as GetMessagesInfraFilters,
)


class GetMessagesFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def to_infra(self) -> GetMessagesInfraFilters:
        return GetMessagesInfraFilters(
            offset=self.offset,
            limit=self.limit,
        )


class GetAllChatsFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def to_infra(self) -> GetAllChatsInfraFilters:
        return GetAllChatsInfraFilters(
            offset=self.offset,
            limit=self.limit,
        )
