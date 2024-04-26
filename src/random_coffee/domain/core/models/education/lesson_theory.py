from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class LessonTheory(BaseRelationalEntity):
    __tablename__ = 'lesson_theory'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"))
    theory_id: Mapped[int] = mapped_column(ForeignKey("theory.id"))
