from typing import Literal

from random_coffee.domain.core.adapters.notification_destination import \
    AllNotificationDestinations
from random_coffee.domain.core.adapters.person import AllPersons
from random_coffee.infrastructure.notifier import Notifier
from random_coffee.infrastructure.security.scopes import AccessScopeEnum

from random_coffee.domain.core.exceptions.notification import (
    PersonHasNoNotificationDestinations,
    NotificationError,
    CantReportInternalError
)

from random_coffee.infrastructure.bases.service import BaseService


class NotificationService(BaseService):
    def __init__(
            self,
            notifier: Notifier,
            all_persons: AllPersons,
            all_notification_destinations: AllNotificationDestinations,
    ):
        self.notifier = notifier
        self.all_persons = all_persons
        self.all_notification_destinations = all_notification_destinations

    async def notify_person(
            self,
            person_id: int,
            notification_content: str,
            on_no_destinations: Literal['ignore', 'raise'] = 'raise',
    ):
        destinations = await self.all_notification_destinations.get_by_person(
            person_id=person_id,
            order_by_priority_desc=True,
        )
        destinations = list(destinations)

        if len(destinations) == 0:
            if on_no_destinations == 'ignore':
                return None
            elif on_no_destinations == 'raise':
                raise PersonHasNoNotificationDestinations(person_id)
            else:
                raise TypeError(on_no_destinations)

        most_relevant = destinations[0]

        await self.notifier.send_notification(
            backend_enum_member=most_relevant.notifier_backend,
            internal_destination_identifier=most_relevant.internal_identifier,
            notification_content=notification_content,
        )
