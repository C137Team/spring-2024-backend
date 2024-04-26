from random_coffee.domain.core.models.education.lesson import Lesson
from random_coffee.domain.core.models.education.lesson_theory import LessonTheory
from random_coffee.domain.core.models.education.theory import Theory
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllLessonTheory(BaseEntityRepo[LessonTheory]):
    async def create_link(
            self,
            lesson: Lesson,
            theory: Theory
    ):
        obj = LessonTheory(
            lesson_id=lesson.id,
            theory=theory.id
        )
        await self.save(obj)
        return obj

