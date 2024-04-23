from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.services import (
    AuthenticationService,
    IdentificationService,
)

from .dto import UpsertTelegramEntitiesDTO, UpsertTelegramEntitiesResponseDTO
from ...domain.core.adapters.person import AllPersons
from ...domain.telegram.services import DatabaseSyncService


class UpsertTelegramEntities(UseCase[UpsertTelegramEntitiesDTO, UpsertTelegramEntitiesResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            all_persons: AllPersons,
            authentication_service: AuthenticationService,
            identification_service: IdentificationService,
            telegram_database_sync_service: DatabaseSyncService,
    ):
        self.telegram_database_sync_service = telegram_database_sync_service
        self.all_persons = all_persons
        self.authentication_service = authentication_service
        self.identification_service = identification_service

    async def __call__(self, payload: UpsertTelegramEntitiesDTO) -> UpsertTelegramEntitiesResponseDTO:
        if payload.user is not None:
            await self.telegram_database_sync_service.visit_user(payload.user)
        if payload.chat is not None:
            await self.telegram_database_sync_service.visit_chat(payload.chat)

        return UpsertTelegramEntitiesResponseDTO(
        )
