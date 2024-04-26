from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.models.education.lesson import Lesson
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllLessons(BaseEntityRepo[Lesson]):
    async def create(
            self,
            course_id: int
    ) -> Lesson:
        obj = Lesson(
            course_id=course_id,
        )
        await self.save(obj)
        return obj

    async def all_by_course(
            self,
            course_id: int
    ) -> Iterable[Lesson]:
        stmt = (select(Lesson)
                .where(Lesson.course_id == course_id)
                .order_by(Lesson.finished.desc()))

        return await self.session.scalars(stmt)

    async def delete(
            self,
            _id: int
    ) -> None:
        return await self.delete_by_id(_id)

