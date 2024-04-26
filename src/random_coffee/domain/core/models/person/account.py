from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship

from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity

if TYPE_CHECKING:
    from random_coffee.domain.core.models.person.person import Person


class AccountId(int, BuiltinSubtypeMixin):
    pass


class Account(BaseRelationalEntity):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    person: Mapped[Optional[Person]] = relationship()
