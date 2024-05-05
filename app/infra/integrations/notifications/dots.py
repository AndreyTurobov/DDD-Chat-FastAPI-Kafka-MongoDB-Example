from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    # TODO: add user_id
    title: str
    text: str
