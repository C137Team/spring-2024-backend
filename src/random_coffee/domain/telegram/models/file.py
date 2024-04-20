from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class File(BaseRelationalEntity):
    __tablename__ = 'telegram_file'

    id: Mapped[str] = mapped_column(primary_key=True)
    size: Mapped[int] = mapped_column()
    path: Mapped[str] = mapped_column(unique=True)
    from_chat_id: Mapped[int] = mapped_column(ForeignKey("telegram_chat.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
