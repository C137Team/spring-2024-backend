from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from typing_extensions import TypeAlias

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity

if TYPE_CHECKING:
    from random_coffee.domain.core.models.employee import Employee


class GroupId(int, BuiltinSubtypeMixin):
    pass


class Organisation(BaseRelationalEntity):
    __tablename__ = 'organisation'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    email_domain: Mapped[str] = mapped_column()

    employees: Mapped[list[Employee]] = relationship(back_populates="organisation")

    def __str__(self):  # for admin panel
        return f"{self.title}"
