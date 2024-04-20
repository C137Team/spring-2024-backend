from __future__ import annotations

from typing import Optional, Iterable

from sqlalchemy import select, delete, and_

from random_coffee.domain.core.models import NotificationDestination
from random_coffee.domain.core.models.notification_destination import \
    NotificationDestinationRelPerson
from random_coffee.domain.core.models.organisation import Organisation
from random_coffee.infrastructure.notifier.interface import NotifierBackendEnum
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllOrganisations(BaseEntityRepo[Organisation]):
    async def get_by_email_domain(
            self,
            o: str,
    ):
        stmt = (select(Organisation)
                .where(Organisation.email_domain == o))
        await self.session.scalars(stmt)
