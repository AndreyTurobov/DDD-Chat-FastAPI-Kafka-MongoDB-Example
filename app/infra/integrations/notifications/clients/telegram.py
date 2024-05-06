from dataclasses import dataclass

from httpx._client import AsyncClient

from infra.integrations.notifications.clients.base import BaseNotificationClient
from infra.integrations.notifications.dtos import Notification


@dataclass
class TelegramNotificationClient(BaseNotificationClient):
    bot_token: str
    chat_id: str
    http_client: AsyncClient
    send_url: str

    async def _format_notification(self, notification: Notification) -> str:
        return f"{notification.title}\n{notification.text}\n"

    async def send(self, notification: Notification):
        await self.http_client.get(
            url=f"{self._host}/bot{self.bot_token}/sendMessage",
            params={
                "chat_id": self.chat_id,
                "text": self._format_notification(notification=notification),
            },
        )
