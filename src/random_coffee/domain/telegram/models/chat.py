from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.infrastructure.database import TelegramIdentifier
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity
from .chat_member import ChatMember


if TYPE_CHECKING:
    from .telegramaccount import TelegramAccount


class Chat(BaseRelationalEntity):
    __tablename__ = 'telegram_chat'

    id: Mapped[TelegramIdentifier] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    title: Mapped[str | None] = mapped_column()
    username: Mapped[str | None] = mapped_column()
    invitation_link: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    members: Mapped[list[TelegramAccount]] = relationship(secondary=ChatMember.__table__)
