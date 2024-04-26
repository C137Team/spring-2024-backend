from sqlalchemy import VARCHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.domain.core.models.person.achievement_type import AchievementType
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class Achievement(BaseRelationalEntity):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[AchievementType] = mapped_column(Enum(AchievementType))
    title: Mapped[str] = mapped_column(VARCHAR(25))
    description: Mapped[str] = mapped_column(VARCHAR(256))
    image: Mapped[str] = mapped_column(VARCHAR(256))
