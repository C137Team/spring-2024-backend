from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.models.education.course import Course
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllCourses(BaseEntityRepo[Course]):
    async def create(
            self,
            educational_material_id: int,
            person_id: int
    ) -> Course:
        obj = Course(
            educational_material_id=educational_material_id,
            person_id=person_id
        )
        await self.save(obj)
        return obj

    async def all_by_person(
            self,
            person_id: int,
            finished: bool = None
    ) -> Iterable[Course]:
        stmt = (select(Course)
                .where(Course.person_id == person_id))

        if finished is not None:
            stmt.where(Course.finished == finished)

        return await self.session.scalars(stmt)

    async def delete(
            self,
            _id: int
    ) -> None:
        return await self.delete_by_id(_id)
