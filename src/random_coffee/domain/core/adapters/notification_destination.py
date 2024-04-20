from __future__ import annotations

from typing import Optional, Iterable

from sqlalchemy import select, delete, and_

from random_coffee.domain.core.models import NotificationDestination
from random_coffee.domain.core.models.notification_destination import \
    NotificationDestinationRelPerson
from random_coffee.domain.core.models.person import Person
from random_coffee.infrastructure.notifier.interface import NotifierBackendEnum
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllNotificationDestinations(BaseEntityRepo[NotificationDestination]):
    async def get_by_value(
            self,
            notifier_backend: NotifierBackendEnum,
            internal_identifier: str,
    ) -> Optional[NotificationDestination]:
        stmt = (select(NotificationDestination)
                .where(NotificationDestination.notifier_backend
                       == notifier_backend)
                .where(NotificationDestination.internal_identifier
                       == internal_identifier))
        result = await self.session.scalar(stmt)

        return result

    async def create(
            self,
            notifier_backend: NotifierBackendEnum,
            internal_identifier: str,
            priority: int,
    ) -> NotificationDestination:
        obj = NotificationDestination(
            notifier_backend=notifier_backend,
            internal_identifier=internal_identifier,
            priority=priority,
        )
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def attach_to_person(
            self,
            notification_destination_id: int,
            person_id: int,
    ) -> NotificationDestinationRelPerson:
        obj = NotificationDestinationRelPerson(
            notification_destination_id=notification_destination_id,
            person_id=person_id,
        )
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def detach_from_all_persons(
            self,
            notification_destination_id: int,
    ) -> None:
        model = NotificationDestinationRelPerson
        stmt = (delete(model)
                .where(model.notification_destination_id
                       == notification_destination_id))
        await self.session.execute(stmt)
        return None

    async def get_by_person(
            self,
            person_id: int,
            order_by_priority_desc: bool = False,
    ) -> Iterable[NotificationDestination]:
        stmt = (select(NotificationDestination)
                .join(NotificationDestinationRelPerson,
                      and_(NotificationDestinationRelPerson.person_id == person_id,
                           NotificationDestination.id == NotificationDestinationRelPerson.notification_destination_id)))
        if order_by_priority_desc:
            stmt = (stmt
                    .order_by(NotificationDestination.priority.desc()))

        result = await self.session.execute(stmt)
        result = result.scalars()

        return result
