from pydantic import BaseModel

from infra.repositories.filters.messages import GetMessagesFilters as GetMessagesInfraFilters


class GetMessagesFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def to_infra(self):
        return GetMessagesInfraFilters(
            offset=self.offset,
            limit=self.limit,
        )
