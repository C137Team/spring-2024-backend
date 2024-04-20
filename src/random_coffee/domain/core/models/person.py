from __future__ import annotations

from typing import Optional, Union, TYPE_CHECKING
from typing_extensions import TypeAlias

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity
from .meeting_format import MeetingFormatEnum

if TYPE_CHECKING:
    from random_coffee.domain.core.models import Account


class PersonId(int, BuiltinSubtypeMixin):
    pass


class Person(BaseRelationalEntity):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    account_id: Mapped[Optional[int]] = mapped_column(ForeignKey('account.id'))
    telegram_account_id: Mapped[Optional[int]] = mapped_column(ForeignKey("telegram_account.id"))
    full_name: Mapped[str] = mapped_column()
    age: Mapped[int | None] = mapped_column()
    post: Mapped[str | None] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    meeting_max_participant_count: Mapped[int] = mapped_column(server_default="2")
    meeting_preferred_format: Mapped[MeetingFormatEnum | None] = mapped_column(default=None)

    def __str__(self):  # for admin panel
        return f'{self.full_name}'

    __repr__ = __str__  # for debug
