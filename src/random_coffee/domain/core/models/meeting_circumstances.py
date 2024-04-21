from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from typing_extensions import TypeAlias

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.domain.core.models.meeting_format import MeetingFormatEnum
from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity

if TYPE_CHECKING:
    from random_coffee.domain.core.models import Person


class MeetingCircumstancesId(int, BuiltinSubtypeMixin):
    pass


class MeetingCircumstances(BaseRelationalEntity):
    __tablename__ = 'meeting_circumstances'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    starts_at: Mapped[datetime] = mapped_column()
    duration_m: Mapped[int] = mapped_column()
    format: Mapped[MeetingFormatEnum] = mapped_column()
    location_latitude: Mapped[float] =  mapped_column()
    location_longutude: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __str__(self):  # for admin panel
        return f"from {self.starts_at} for {self.duration_m} min"
