from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.infrastructure.models import BuiltinSubtypeMixin
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity

from .meeting_state import MeetingStateEnum

if TYPE_CHECKING:
    from .meeting_participant import MeetingParticipant
    from .meeting_circumstances import MeetingCircumstances


class MeetingId(int, BuiltinSubtypeMixin):
    pass


class Meeting(BaseRelationalEntity):
    __tablename__ = 'meeting'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state: Mapped[MeetingStateEnum] = mapped_column("Enum(MeetingStateEnum)")
    circumstances_id: Mapped[Optional[int]] = mapped_column(ForeignKey("meeting_circumstances.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column()

    participants: Mapped[list[MeetingParticipant]] = relationship(back_populates="meeting")
    circumstances: Mapped[MeetingCircumstances] = relationship()
