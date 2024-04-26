from datetime import datetime

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class Course(BaseRelationalEntity):
    __tablename__ = 'course'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    educational_material_id: Mapped[int] = mapped_column(ForeignKey("educational_material.id"))
    finished: Mapped[bool] = mapped_column(Boolean(), default=False)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    start_date: Mapped[datetime] = mapped_column(default=datetime.now)
    end_date: [datetime | None] = mapped_column(default=None)

