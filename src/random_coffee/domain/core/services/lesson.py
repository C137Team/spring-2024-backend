from typing import Iterable

from random_coffee.domain.core.adapters.lesson import AllLessons
from random_coffee.domain.core.models.education.course import Course
from random_coffee.domain.core.models.education.lesson import Lesson
from random_coffee.infrastructure.service import BaseService


class LessonService(BaseService):
    def __init__(
            self,
            all_lessons: AllLessons
    ):
        self.all_lessons = all_lessons

    async def create(
            self,
            course: Course
    ) -> Lesson:
        return await self.all_lessons.create(course.id)

    async def all_by_course(
            self,
            course: Course,
    ) -> Iterable[Lesson]:
        return await self.all_lessons.all_by_course(course.id)

    async def delete(
            self,
            _id: int
    ) -> None:
        return await self.delete_by_id(_id)