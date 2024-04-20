from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.adapters.person import (
    AllPersons,
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
    ):
        self.all_telegram_accounts = all_telegram_accounts
        self.all_persons = all_persons
        self.telegram_s = telegram_s

    async def __call__(
            self, payload: AttachPersonToTelegramAccountDTO
    ) -> AttachPersonToTelegramAccountResponseDTO:
        telegram_account = await self.all_telegram_accounts.with_id(
            id_=payload.telegram_account_id,
        )
        person = await self.all_persons.with_id(
            payload.person_id,
        )
        person.telegram_account_id = telegram_account.id

        return AttachPersonToTelegramAccountResponseDTO(
        )
