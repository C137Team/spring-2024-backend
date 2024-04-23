from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from random_coffee.domain.core import models
from random_coffee.infrastructure.notifier.interface import NotifierBackendEnum
from random_coffee.domain.core.models import (
    Person,
    Account,
    UTM,
    NotificationDestination,
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
            description=model.description,
            display_text=model.full_name,
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
