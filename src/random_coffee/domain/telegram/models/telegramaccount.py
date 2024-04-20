from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.domain.core.models import Person
from random_coffee.infrastructure.database import TelegramIdentifier
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class TelegramAccount(BaseRelationalEntity):
    __tablename__ = 'telegram_account'

    id: Mapped[TelegramIdentifier] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    username: Mapped[str | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    person: Mapped[Person | None] = relationship()
