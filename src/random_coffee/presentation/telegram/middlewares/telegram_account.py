from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from random_coffee.application.merge_telegram_account import MergeTelegramAccountDTO, MergeTelegramAccountResponseDTO
from random_coffee.presentation.interactor_factory.telegram import TelegramInteractorFactory
from random_coffee.presentation.telegram.errors.auth import AccountNotIdentifiedError


class TelegramAccountMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        telegram_ioc: TelegramInteractorFactory = data.get('telegram_ioc')
        event_from_user: User = data.get('event_from_user')

        if event_from_user is not None:
            async with telegram_ioc.merge_telegram_account() as use_case:
                response = await use_case(
                    MergeTelegramAccountDTO(
                        telegram_id=event_from_user.id,
                        username=event_from_user.username,
                        first_name=event_from_user.first_name,
                        last_name=event_from_user.last_name,
                    )
                )

            telegram_account = response.telegram_account

            data.update({
                "telegram_account": telegram_account,
                "cached_person": telegram_account.person,
            })

        return await handler(event, data)


telegram_account_middleware = TelegramAccountMiddleware()
