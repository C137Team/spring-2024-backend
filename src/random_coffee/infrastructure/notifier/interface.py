from typing import Any, Iterable

from enum import Enum

from .backends.base import NotifierBackend


class NotifierBackendEnum(Enum):
    TELEGRAM = 'TELEGRAM'
    EMAIL = 'EMAIL'


class Notifier:
    def __init__(self,
                 backends: list[NotifierBackend]):

        self._backends: dict[NotifierBackendEnum, NotifierBackend] = {
            NotifierBackendEnum(i.get_enum_value()): i
            for i in backends
        }

    async def send_notification(self,
                                backend_enum_member: NotifierBackendEnum,
                                internal_destination_identifier: str,
                                notification_content: Any,
                                priority: int | None = None) -> Any:

        backend = self._backends[backend_enum_member]
        backend_response = backend.send_notification(
            internal_destination_identifier=internal_destination_identifier,
            notification_content=notification_content,
            priority=priority,
        )

        return backend_response

    async def broadcast_notification(
            self,
            backend_enum_member: NotifierBackendEnum,
            internal_destination_identifiers: Iterable[str],
            notification_content: Any,
            priority: int | None = None,
    ):
        backend = self._backends[backend_enum_member]
        backend_response = backend.broadcast_notification(
            internal_destination_identifiers=internal_destination_identifiers,
            notification_content=notification_content,
            priority=priority,
        )

        return backend_response
