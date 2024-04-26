from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class Theory(BaseRelationalEntity):
    __tablename__ = 'theory'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"))
    title: Mapped[str] = mapped_column(VARCHAR(30))
    content: Mapped[str] = mapped_column()
