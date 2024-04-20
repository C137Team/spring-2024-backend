from typing import Optional

from sqlalchemy import select, func

from random_coffee.domain.core.models import NotificationDestination
from random_coffee.domain.core.models.account import Account
from random_coffee.domain.core.models.person import Person
from random_coffee.infrastructure.notifier import NotifierBackendEnum
from random_coffee.infrastructure.notifier.backends.base import NotifierBackend
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllAccounts(BaseEntityRepo[Account]):
    async def is_email_occupied(
            self,
            login: str,
    ) -> bool:
        stmt = (select(func.count(Account.id))
                .where(Account.email == login))
        result = await self.session.execute(stmt)
        result = result.scalar_one()
        result = result > 0

        return result

    async def create(
            self,
            email: str,
            password_hash: str,
            person: Optional[Person] = None,
    ) -> Account:
        obj = Account(
            email=email,
            password_hash=password_hash,
            person=person,
        )
        self.session.add_all((
            obj,
        ))
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def with_login(
            self,
            login: str,
    ) -> Optional[Account]:
        stmt = (select(Account)
                .where(Account.email == login))
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()

        return result
