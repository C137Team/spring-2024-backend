from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


UTMId = UUID


class UTM(BaseRelationalEntity):
    __tablename__ = 'utm'

    id: Mapped[UTMId] = mapped_column(default=uuid4, primary_key=True)
    value: Mapped[Optional[str]] = mapped_column()
    expire_at: Mapped[datetime] = mapped_column()
    read_limit: Mapped[int] = mapped_column()
    read_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
