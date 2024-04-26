from datetime import datetime

from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.domain.core.models.education.tag import Tag
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class EducationalMaterial(BaseRelationalEntity):
    __tablename__ = 'education_material'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(25))
    description: Mapped[str] = mapped_column(VARCHAR(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    tags: Mapped[Tag] = relationship(lazy='selectin')
