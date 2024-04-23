from __future__ import annotations

from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.models import PersonAchievement
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllPersonsAchievements(BaseEntityRepo[PersonAchievement]):
    async def create(
            self,
            achievement_id: int,
            person_id: int,
    ):
        obj = PersonAchievement(
            achievement_id=achievement_id,
            person_id=person_id,
        )
        await self.save(obj)
        return obj

    async def with_person_id(
            self,
            person_id: int,
    ) -> Iterable[PersonAchievement]:
        stmt = (select(PersonAchievement)
                .where(PersonAchievement.person_id == person_id))
        return await self.session.scalars(stmt)
