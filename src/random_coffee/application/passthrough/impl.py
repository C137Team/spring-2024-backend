from random_coffee.domain.core.adapters.employee import AllEmployees
from random_coffee.domain.core.adapters.meeting import AllMeetings
from random_coffee.domain.core.adapters.wandering_employee import (
    AllWanderingEmployees,
)
from random_coffee.domain.core.services.meeting import MeetingService
from random_coffee.infrastructure.service import BaseService


class Passthrough(BaseService):
    def __init__(
            self,
            all_meetings: AllMeetings,
            meeting_service: MeetingService,
            all_wandering_employes: AllWanderingEmployees,
            all_employees: AllEmployees,
    ):
        self.all_meetings = all_meetings
        self.meeting_service = meeting_service
        self.all_wandering_employes = all_wandering_employes
        self.all_employees = all_employees
