from __future__ import annotations

from sqlalchemy import select

from random_coffee.domain.core.models import Meeting, Person
from random_coffee.domain.core.models.meeting_participant import \
    MeetingParticipant
from random_coffee.domain.core.models.meeting_state import MeetingStateEnum
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllMeetings(BaseEntityRepo[Meeting]):
    async def active_for_person(self, person_id: int):
        stmt = (select(Meeting)
                .join(MeetingParticipant)
                .join(Person)
                .where(Meeting.state.in_((MeetingStateEnum.PLANNED,
                                          MeetingStateEnum.SCHEDULED,
                                          MeetingStateEnum.OCCUR)))
                .where(Person.id == person_id))
        return await self.session.scalar(stmt)
