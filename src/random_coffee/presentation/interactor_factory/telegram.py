from __future__ import annotations

from random_coffee import application
from random_coffee.infrastructure.bases.interactor_factory import (
    BaseInteractorFactory,
    use_case_wrapper,
    WiredUseCase,
)


class TelegramInteractorFactory(BaseInteractorFactory):
    @use_case_wrapper[application.merge_telegram_account.MergeTelegramAccount]()
    async def merge_telegram_account(
            self: TelegramInteractorFactory, use_case: application.merge_telegram_account.MergeTelegramAccount,
    ) -> WiredUseCase[application.merge_telegram_account.MergeTelegramAccount]:
        yield use_case

    @use_case_wrapper[
        application.attach_person_to_telegram_account.AttachPersonToTelegramAccount]()
    async def attach_person_to_telegram_account(
            self: TelegramInteractorFactory,
            use_case: application.attach_person_to_telegram_account.AttachPersonToTelegramAccount,
    ) -> WiredUseCase[application.attach_person_to_telegram_account.AttachPersonToTelegramAccount]:
        yield use_case
