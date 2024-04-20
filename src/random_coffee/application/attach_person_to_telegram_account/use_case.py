from random_coffee.domain.core.services import AuthenticationService
from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.adapters import (
    AllPersons, AllAccounts,
)
from random_coffee.domain.telegram.repos.accounts import (
    AllAccounts as AllTelegramAccounts,
)
from random_coffee.domain.telegram.services import (
    DatabaseSyncService,
)

from random_coffee.application.attach_person_to_telegram_account.dto import (
    AttachPersonToTelegramAccountDTO, AttachPersonToTelegramAccountResponseDTO
)
from random_coffee.infrastructure.security.token import CreateTokenData, \
    create_access_token, Sub


class AttachPersonToTelegramAccount(
    UseCase[AttachPersonToTelegramAccountDTO,
            AttachPersonToTelegramAccountResponseDTO]
):
    # noinspection PyProtocol
    def __init__(
            self,
            all_telegram_accounts: AllTelegramAccounts,
            all_persons: AllPersons,
            telegram_s: DatabaseSyncService,
            all_accounts: AllAccounts,
            authentication_service: AuthenticationService,

    ):
        self.all_telegram_accounts = all_telegram_accounts
        self.all_persons = all_persons
        self.all_accounts = all_accounts
        self.telegram_s = telegram_s
        self.authentication_service = authentication_service

    async def __call__(
            self, payload: AttachPersonToTelegramAccountDTO
    ) -> AttachPersonToTelegramAccountResponseDTO:
        person_id = int(payload.person_secret)  # todo: adjust
        telegram_account = await self.all_telegram_accounts.with_id(
            id_=payload.telegram_account_id,
        )
        person = await self.all_persons.with_id(
            person_id,
        )
        person.telegram_account_id = telegram_account.id
        account = await self.all_accounts.with_person(person_id)
        access_token = create_access_token(
            create_payload=CreateTokenData(
                sub=Sub(login=account.email),
                scopes=[],
            )
        )
        return AttachPersonToTelegramAccountResponseDTO(
            access_token=access_token,
        )
