from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.database import TelegramIdentifier
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class ChatMember(BaseRelationalEntity):
    __tablename__ = 'telegram_chat_member'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    telegram_account_id: Mapped[TelegramIdentifier] = mapped_column(ForeignKey("telegram_account.id"))
    telegram_chat_id: Mapped[TelegramIdentifier] = mapped_column(ForeignKey("telegram_chat.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
