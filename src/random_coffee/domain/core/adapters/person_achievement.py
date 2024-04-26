from __future__ import annotations

from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.models.person.person_achievement import PersonAchievement
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
            limit: int = 0,
            offset: int = 0
    ) -> Iterable[PersonAchievement]:
        stmt = (select(PersonAchievement)
                .where(PersonAchievement.person_id == person_id)
                .limit(limit)
                .offset(offset))
        return await self.session.scalars(stmt)
