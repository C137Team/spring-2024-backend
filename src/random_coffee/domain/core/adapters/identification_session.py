from typing import Optional, Iterable

from sqlalchemy import select, update

from random_coffee.domain.core.models.identification_session import \
    IdentificationSession, IdentificationSessionStatusEnum
from random_coffee.infrastructure.bases.db_gateway import BaseDbGateway
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllIdentificationSessions(BaseEntityRepo[IdentificationSession]):
    async def create(
            self,
            account_id: int,
            person_id: int,
            organisation_id: int,
            confirmation_code_hash: str,
    ) -> IdentificationSession:
        obj = IdentificationSession(
            account_id=account_id,
            person_id=person_id,
            organisation_id=organisation_id,
            confirmation_code_hash=confirmation_code_hash,
        )
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def set_status(
            self,
            identification_session_id: int,
            status: IdentificationSessionStatusEnum,
    ) -> None:
        stmt = (update(IdentificationSession)
                .where(IdentificationSession.id == identification_session_id)
                .values(status=status))
        await self.session.execute(stmt)

        return None

    async def by_account(
            self,
            account_id: int,
    ):
        stmt = (select(IdentificationSession)
                .where(IdentificationSession.account_id == account_id))
        return await self.session.scalars(stmt)
