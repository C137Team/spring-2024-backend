from random_coffee.infrastructure.bases.use_case import UseCase

from .dto import CleanupWanderingDTO, CleanupWanderingResponseDTO
from ...domain.core.adapters.employee import AllEmployees
from ...domain.core.adapters.wandering_employee import AllWanderingEmployees
from ...domain.core.services.matching import MatchingStrategyFullyBatched
from ...domain.core.services.meeting import MeetingService


class CleanupWandering(
    UseCase[
        CleanupWanderingDTO,
        CleanupWanderingResponseDTO,
    ]
):
    # noinspection PyProtocol
    def __init__(
            self,
            matching_strategy: MatchingStrategyFullyBatched,
            meeting_service: MeetingService,
            all_employees: AllEmployees,
            all_wanderring_employees: AllWanderingEmployees,
    ):
        self.matching_strategy = matching_strategy
        self.meeting_service = meeting_service
        self.all_employees = all_employees
        self.all_wanderring_employees = all_wanderring_employees

    async def __call__(
            self, payload: CleanupWanderingDTO
    ) -> CleanupWanderingResponseDTO:
        await self.meeting_service.cleanup_wonderring_employees(
            organisation_id=payload.organisation_id,
        )
        return CleanupWanderingResponseDTO(
        )
