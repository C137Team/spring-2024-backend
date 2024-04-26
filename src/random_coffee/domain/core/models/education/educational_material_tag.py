from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class EducationalMaterialTag(BaseRelationalEntity):
    __tablename__ = 'education_material_tag'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    educational_material_id: Mapped[int] = mapped_column(ForeignKey("education_material.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"))
