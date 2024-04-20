from typing import Iterable, Any
from celery import Celery
from ..base import NotifierBackend

from .tasks import send_email_task, EmailNotificationContentDTO


app = Celery()


app.config_from_object("random_coffee.celeryconfig")


class EmailNotifierBackend(NotifierBackend):
    def __init__(self):
        pass

    def get_enum_value(self) -> str:
        return "EMAIL"

    def send_notification(self,
                          internal_destination_identifier: str,
                          notification_content: EmailNotificationContentDTO,
                          priority: int | None = None) -> None:
        if isinstance(notification_content, str):
            notification_content = EmailNotificationContentDTO(
                text=notification_content,
            )
        dumped_content = notification_content.model_dump_json()
        task = send_email_task.apply_async(
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
        tasks = []
        for i in internal_destination_identifiers:
            tasks.append(self.send_notification(
                internal_destination_identifier=i,
                notification_content=dumped_content,
                priority=priority,
            ))
        return tasks
