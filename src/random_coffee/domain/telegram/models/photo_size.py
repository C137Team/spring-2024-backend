from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.database import TelegramIdentifier
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class PhotoSize(BaseRelationalEntity):
    __tablename__ = 'telegram_photo_size'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(unique=True)  # may be not presented in files table
    file_size: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    width: Mapped[int] = mapped_column()
    from_chat_id: Mapped[TelegramIdentifier] = mapped_column(ForeignKey("telegram_account.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
