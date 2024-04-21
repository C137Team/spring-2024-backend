from itertools import islice
from typing import AbstractSet

from random_coffee.domain.core.adapters.meeting import AllMeetings
from random_coffee.domain.core.adapters.wandering_employee import \
    AllWanderingEmployees
from random_coffee.domain.core.models import Meeting, Person, Employee
from random_coffee.domain.core.models.matching_group import MatchingGroup
from random_coffee.domain.core.models.meeting_participant import \
    MeetingParticipant
from random_coffee.domain.core.models.wandering_employee import \
    WanderingEmployee
from random_coffee.domain.core.services.matching import MatchingStrategy, \
    MatchingStrategyFullyBatched
from random_coffee.domain.core.services.notification import NotificationService
from random_coffee.infrastructure.service import BaseService
from random_coffee.infrastructure.value_object import BaseVO


class MeetingService:
    def __init__(
            self,
            matching_strategy: MatchingStrategyFullyBatched,
            all_wandering_employees: AllWanderingEmployees,
            all_meetings: AllMeetings,
            notification_service: NotificationService,
    ):
        self.matching_strategy = matching_strategy
        self.all_wandering_employees = all_wandering_employees
        self.all_meetings = all_meetings
        self.notification_service = notification_service

    async def cleanup_wonderring_employees(
            self,
            organisation_id: int,
    ):
        wonderring = await self.all_wandering_employees.within_organisation(
            organisation_id=organisation_id,
        )
        matching_group = MatchingGroup(
            employees=[i.employee for i in wonderring]
        )
        result = await self.matching_strategy(matching_group)

        for i in result.planned_meetings:
            persons = [j.employee.person for j in i.participants]
            for j in persons:
                others = set(persons) - {j}

                await self.notification_service.notify_person(
                    person_id=j.id,
                    notification_content=
                    f"У вас новый мэтч! Это {', '.join(others)}"
                )
        for i in result.unmatched_employees:
            await self.notification_service.notify_person(
                person_id=i.id,
                notification_content=
                f"К сожалению, не смогла найти для вас коллегу для "
                f"втречи. Попробуйте поискать позже"
            )

        await self.all_meetings.save_all(list(result.planned_meetings))
        await self.all_meetings.commit()

    async def wander_meeting(
            self,
            employee_id: int,
    ):
        wanderring = await self.all_wandering_employees.with_employee_id(employee_id)
        if wanderring is None:
            new_w = WanderingEmployee(
                employee_id=employee_id,
            )
            await self.all_wandering_employees.save(new_w)
