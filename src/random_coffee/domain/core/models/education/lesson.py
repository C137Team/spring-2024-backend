from datetime import datetime

from sqlalchemy import ForeignKey, Boolean, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from random_coffee.domain.core.models.education.theory import Theory
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class Lesson(BaseRelationalEntity):
    __tablename__ = 'lesson'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(30))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    finished: Mapped[bool] = mapped_column(Boolean(), default=False)
    start_date: Mapped[datetime] = mapped_column(default=datetime.now)
