import logging
import smtplib
from email.message import EmailMessage

from celery import shared_task

from random_coffee.infrastructure.dto import BaseDTO

from random_coffee.infrastructure.config import environment

logger = logging.getLogger(__name__)


class EmailNotificationContentDTO(BaseDTO):
    text: str


def _execute(
        destination_email_address: str,
        content: EmailNotificationContentDTO,
):
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = environment.email_address
    msg['To'] = destination_email_address
    msg.set_content(content.text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(environment.email_address, environment.email_password)
        smtp.send_message(msg)


@shared_task(default_retry_delay=45,  max_retries=10, rate_limit='3/s')
def send_email_task(
        internal_destination_identifier: str,
        notification_content: str,
):
    notification_content = EmailNotificationContentDTO.model_validate_json(notification_content)

    _execute(
        destination_email_address=internal_destination_identifier,
        content=notification_content,
    )

    return {
        "response": "ok",
        "internal_destination_identifier": str(internal_destination_identifier),
        "notifier_backend": "EMAIL",
    }
