from typing import Annotated

from fastapi import APIRouter, Depends

from random_coffee.application.common.dto import PersonDTO, MeetingDTO, \
    EmployeeDTO
from random_coffee.infrastructure.dto import BaseDTO
from random_coffee.presentation.api import dependencies
from random_coffee.presentation.api.dependencies.ioc import CoreIoCDep


router = APIRouter(tags=["Me"])


class GetMyMeetingDTO(BaseDTO):
    meeting: MeetingDTO | None


class EditMyMeetingDTO(BaseDTO):
    set_location_longitude: float | None = None
    set_location_latitude: float | None = None
    set_datetime: float | None
    action_cancel: bool = False


@router.get(
    "/me/meeting",
    response_model=GetMyMeetingDTO,
)
async def get_my_meeting(
        person: Annotated[PersonDTO, Depends(dependencies.get_current.get_current_person)],
        ioc: CoreIoCDep,
):
    async with ioc.passthrough() as ps:
        meeting = await ps.all_meetings.active_for_person(
            person_id=person.id,
        )
        meeting_model = await MeetingDTO.from_model(meeting)

    return meeting_model


@router.post(
    "/me/meeting/edit",
    response_model=GetMyMeetingDTO,
)
async def edit_my_meeting(
        person: Annotated[PersonDTO, Depends(dependencies.get_current.get_current_person)],
        ioc: CoreIoCDep,
):
    async with ioc.passthrough() as ps:
        meeting = await ps.all_meetings.active_for_person(
            person_id=person.id,
        )
        meeting_model = await MeetingDTO.from_model(meeting)

    return meeting_model


class WanderMyMeetingResponseDTO(BaseDTO):
    pass


@router.post(
    "/me/meeting/wander",
    response_model=WanderMyMeetingResponseDTO,
)
async def wander_my_meeting(
        person: Annotated[PersonDTO, Depends(dependencies.get_current.get_current_person)],
        employee: Annotated[EmployeeDTO, Depends(dependencies.get_current.get_current_employee)],
        ioc: CoreIoCDep,
):
    async with ioc.passthrough() as ps:
        response = await ps.meeting_service.wander_meeting(
            employee_id=employee.id,
        )
    return WanderMyMeetingResponseDTO(

    )
