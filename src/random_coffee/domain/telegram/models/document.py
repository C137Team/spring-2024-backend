from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.database import TelegramIdentifier
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class Document(BaseRelationalEntity):
    __tablename__ = 'document'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(unique=True)  # may be not presented in files table
    file_size: Mapped[int] = mapped_column()
    from_chat_id: Mapped[TelegramIdentifier] = mapped_column(ForeignKey("telegram_account.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
