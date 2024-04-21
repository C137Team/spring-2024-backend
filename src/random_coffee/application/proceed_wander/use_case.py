from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.services import (
    UTMService,
)
from random_coffee.application.common.dto import (
    UTMDTO,
)

from .dto import ProceedWanderDTO, ProceedWanderResponseDTO
from ...domain.core.adapters.employee import AllEmployees
from ...domain.core.adapters.meeting import AllMeetings
from ...domain.core.adapters.wandering_employee import AllWanderingEmployees
from ...domain.core.models.wandering_employee import WanderingEmployee
from ...domain.core.services.matching import MatchingStrategyFullyBatched
from ...domain.core.services.meeting import MeetingService


class ProceedWander(
    UseCase[
        ProceedWanderDTO,
        ProceedWanderResponseDTO,
    ]
):
    # noinspection PyProtocol
    def __init__(
            self,
            matching_strategy: MatchingStrategyFullyBatched,
            meeting_service: MeetingService,
            all_employees: AllEmployees,
            all_wanderring_employees: AllWanderingEmployees,
            all_meetings: AllMeetings,
    ):
        self.all_meetings = all_meetings
        self.matching_strategy = matching_strategy
        self.meeting_service = meeting_service
        self.all_employees = all_employees
        self.all_wanderring_employees = all_wanderring_employees

    async def __call__(
            self, payload: ProceedWanderDTO
    ) -> ProceedWanderResponseDTO:
        non_wandering = await self.all_employees.wich_doesnt_wandering(
            organisation_id=payload.organisation_id,
        )
        non_wandering = list(non_wandering)
        for i in non_wandering:
            my_meet = await self.all_meetings.active_for_person(
                i.person_id,
            )
            if my_meet is not None:
                continue
            wandering = WanderingEmployee(
                employee=i,
            )
            await self.all_wanderring_employees.save(wandering)
        await self.all_wanderring_employees.commit()

        return ProceedWanderResponseDTO(
            total_wanderring=len(non_wandering),
        )
