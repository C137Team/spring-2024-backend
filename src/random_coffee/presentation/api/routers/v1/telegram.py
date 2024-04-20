import aiogram
from fastapi import APIRouter

from random_coffee.application.attach_person_to_telegram_account import \
    AttachPersonToTelegramAccountDTO, AttachPersonToTelegramAccountResponseDTO
from random_coffee.application.upsert_telegram_entities import \
    UpsertTelegramEntitiesDTO, UpsertTelegramEntitiesResponseDTO
from random_coffee.infrastructure.dto import BaseDTO
from random_coffee.presentation.api.dependencies.ioc import TelegramIoCDep
from random_coffee.presentation.interactor_factory import \
    CoreInteractorFactory, TelegramInteractorFactory

router = APIRouter()


class ConnectTelegramAccountDTO(BaseDTO):
    telegram_id: int


@router.post(
    "/me/telegram/account/attach",
    response_model=AttachPersonToTelegramAccountResponseDTO,
)
async def attach_telegram_account(
        payload: AttachPersonToTelegramAccountDTO,
        telegram_ioc: TelegramIoCDep,
):
    async with telegram_ioc.attach_person_to_telegram_account() as use_case:
        response = await use_case(payload)

    return response


class UpsertTelegramEntities(BaseDTO):
    user: aiogram.types.User | None = None
    chat: aiogram.types.Chat | None = None


@router.post(
    "/internal/telegram/upsert",
    response_model=UpsertTelegramEntitiesResponseDTO,
)
async def upsert_telegram_user(
        payload: UpsertTelegramEntitiesDTO,
        telegram_ioc: TelegramIoCDep,
):
    async with telegram_ioc.upsert_telegram_entities() as use_case:
        response = await use_case(payload)
    return response
