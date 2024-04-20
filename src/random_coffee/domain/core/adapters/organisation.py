from __future__ import annotations

from sqlalchemy import select

from random_coffee.domain.core.models.organisation import Organisation
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllOrganisations(BaseEntityRepo[Organisation]):
    async def get_by_email_domain(
            self,
            o: str,
    ):
        stmt = (select(Organisation)
                .where(Organisation.email_domain == o))
        return await self.session.scalar(stmt)
