from typing import Iterable, Any


from ..base import NotifierBackend

from .tasks import send_telegram_message_task, broadcast_telegram_message_task, TelegramNotificationContentDTO


class TelegramNotifierBackend(NotifierBackend):
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    def get_enum_value(self) -> str:
        return "TELEGRAM"

    def send_notification(self,
                          internal_destination_identifier: str,
                          notification_content: TelegramNotificationContentDTO,
                          priority: int | None = None) -> None:
        dumped_content = notification_content.model_dump_json()
        task = send_telegram_message_task.apply_async(
            kwargs=dict(
                internal_destination_identifier=internal_destination_identifier,
                notification_content=dumped_content,
            ),
            priority=priority,
        )
        return task

    def broadcast_notification(
            self,
            internal_destination_identifiers: Iterable[str],
            notification_content: Any,
            priority: int | None = None
    ) -> Any:
        dumped_content = notification_content.model_dump_json()
        return broadcast_telegram_message_task.apply_async(
            kwargs=dict(
                internal_destination_identifiers=list(internal_destination_identifiers),
                notification_content=dumped_content,
                priority=priority,
            ),
            priority=2,
        )
