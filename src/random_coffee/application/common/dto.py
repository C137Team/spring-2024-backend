from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from random_coffee.domain.core.models.meeting_circumstances import \
    MeetingCircumstances
from random_coffee.domain.core.models.meeting_format import MeetingFormatEnum
from random_coffee.domain.core.models.meeting_participant import \
    MeetingParticipant
from random_coffee.domain.core.models.meeting_state import MeetingStateEnum

from random_coffee.domain.core import models
from random_coffee.infrastructure.notifier.interface import NotifierBackendEnum
from random_coffee.domain.core.models import (
    Person,
    Account,
    UTM,
    NotificationDestination, Role, Employee, Meeting, Organisation,
)
from random_coffee.domain.telegram.models import (
    TelegramAccount as TelegramAccount,
)


BOT_URL = "http://t.me/coffee137_bot"


class PersonDTO(BaseModel):
    id: models.person.PersonId
    full_name: str | None
    age: int | None
    description: str | None
    post: str | None
    attach_telegram_url: str | None
    display_text: str

    @classmethod
    async def from_model(
            cls, model: Person,
    ):
        return cls(
            id=model.id,
            # todo: url security issue
            attach_telegram_url=
            f"{BOT_URL}?start={model.id}"
            if model.telegram_account_id is None
            else None,
            full_name=model.full_name,
            age=model.age,
            description=model.description,
            post=model.post,
            display_text=model.full_name,
        )


class OrganisationDTO(BaseModel):
    id: int
    title: str
    email_domain: str
    display_text: str

    @classmethod
    async def from_model(
            cls, model: Organisation,
    ):
        return cls(
            id=model.id,
            title=model.title,
            email_domain=model.email_domain,
            display_text=model.title,
        )


class MeetingCircumstancesDTO(BaseModel):
    starts_at: datetime
    duration_m: int
    format: MeetingFormatEnum
    location_latitude: float
    location_longitude: float

    @classmethod
    async def from_model(
            cls,
            model: MeetingCircumstances,
    ):
        return cls(
            starts_at=model.starts_at,
            duration_m=model.duration_m,
            format=model.format,
            location_latitude=model.location_latitude,
            location_longutude=model.location_longutude,
        )


class EmployeeDTO(BaseModel):
    id: int
    role: Role
    person: PersonDTO

    @classmethod
    async def from_model(
            cls,
            model: Employee,
    ):
        person = await model.awaitable_attrs.person
        return cls(
            id=model.id,
            role=model.role,
            person=await PersonDTO.from_model(
                model=person,
            )
        )


class MeetingParticipantDTO(BaseModel):
    employee: EmployeeDTO

    @classmethod
    async def from_model(
            cls,
            model: MeetingParticipant,
    ):
        employee = await model.awaitable_attrs.emplyee
        return cls(
            employee=EmployeeDTO.from_model(
                employee,
            )
        )


class MeetingDTO(BaseModel):
    id: int
    state: MeetingStateEnum
    circumstances: MeetingCircumstancesDTO | None
    participants: list[MeetingParticipantDTO]
    created_at: datetime

    @classmethod
    async def from_model(
            cls, model: Meeting,
    ):
        circumstances = await model.awaitable_attrs.circumstances
        return cls(
            id=model.id,
            state=model.state,
            circumstances=circumstances and await MeetingCircumstancesDTO.from_model(
               circumstances,
            ),
            participants=[
                await MeetingParticipantDTO.from_model(
                    i,
                ) for i in await model.awaitable_attrs.participants
            ],
            created_at=model.created_at,
        )


class AccountDTO(BaseModel):
    id: int
    login: str
    person: Optional[PersonDTO]

    @classmethod
    async def from_model(
            cls, model: Account,
    ):
        person = await model.awaitable_attrs.person
        return AccountDTO(
            id=model.id,
            login=model.email,
            person=person and await PersonDTO.from_model(person),
        )


class TelegramAccountDTO(BaseModel):
    id: int
    telegram_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    person: Optional[PersonDTO]

    @classmethod
    async def from_model(
            cls,
            model: TelegramAccount,
    ):
        person = await model.awaitable_attrs.person

        return TelegramAccountDTO(
            id=model.id,
            telegram_id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            username=model.username,
            person=person and PersonDTO.from_model(
                person,
            ),
        )


class UTMDTO(BaseModel):
    id: UUID
    value: Optional[str]
    expire_at: datetime
    remaining_reads: int

    @classmethod
    async def from_model(
            cls,
            model: UTM,
    ):
        return UTMDTO(
            id=model.id,
            value=model.value,
            expire_at=model.expire_at,
            remaining_reads=model.read_limit - model.read_count,
        )


class NotificationDestinationDTO(BaseModel):
    id: int
    notifier_backend: NotifierBackendEnum
    internal_identifier: str
    priority: int

    @classmethod
    async def from_model(
            cls,
            model: NotificationDestination
    ) -> NotificationDestinationDTO:
        return NotificationDestinationDTO(
            id=model.id,
            notifier_backend=model.notifier_backend,
            internal_identifier=model.internal_identifier,
            priority=model.priority,
        )
