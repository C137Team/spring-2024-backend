from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.models.education.theory import Theory
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllTheory(BaseEntityRepo[Theory]):
    async def create(
            self,
            lesson_id: int
    ) -> Theory:
        obj = Theory(
            lesson_id=lesson_id,
        )
        await self.save(obj)
        return obj

    async def all_by_lesson(
            self,
            lesson_id: int
    ) -> Iterable[Theory]:
        stmt = (select(Theory)
                .where(Theory.lesson_id == lesson_id))

        return await self.session.scalars(stmt)

    async def delete(
            self,
            _id: int
    ) -> None:
        return await self.delete_by_id(_id)
