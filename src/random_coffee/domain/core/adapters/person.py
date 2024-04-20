from __future__ import annotations

from random_coffee.domain.core.models.person import Person
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllPersons(BaseEntityRepo[Person]):
    async def create(
            self,
            full_name: str,
    ):
        obj = Person(
            full_name=full_name,
        )
        await self.save(obj)
        return obj
