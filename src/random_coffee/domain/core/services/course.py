from typing import Iterable

from sqlalchemy import select

from random_coffee.domain.core.adapters.course import AllCourses
from random_coffee.domain.core.adapters.lesson import AllLessons
from random_coffee.domain.core.models.education.course import Course
from random_coffee.domain.core.models.education.educational_material import EducationalMaterial
from random_coffee.domain.core.models.person.person import Person
from random_coffee.infrastructure.service import BaseService


class CourseService(BaseService):

    def __init__(
            self,
            all_courses: AllCourses,
            all_lessons: AllLessons
    ):
        self.all_courses = all_courses

    async def create(
            self,
            educational_material: EducationalMaterial,
            person: Person
    ) -> Course:
        return await self.all_courses.create(educational_material.id, person.id)

    async def get_person_courses(
            self,
            person: Person,
            finished: bool = None
    ) -> Iterable[Course]:
        return await self.all_courses.all_by_person(person.id, finished)

    async def delete(
            self,
            course: Course
    ) -> None:
        return await self.all_courses.delete(course.id)
