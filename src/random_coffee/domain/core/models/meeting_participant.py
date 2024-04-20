from __future__ import annotations

from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity

if TYPE_CHECKING:
    from random_coffee.domain.core.models import Meeting, Employee


class MeetingParticipant(BaseRelationalEntity):
    __tablename__ = "meeting_participant"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    emplyee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    meeting: Mapped[Meeting] = relationship()
    employee: Mapped[Employee] = relationship()

    __table_args__ = (
        UniqueConstraint(
            "meeting_id", "emplyee_id",
        ),
    )
