from typing import Callable, Dict, Any, Awaitable, cast

from aiogram import BaseMiddleware
from aiogram.dispatcher import flags
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.event.event import HandlerObject

from random_coffee.domain.core.exceptions.authorization import AuthorizationError
from random_coffee.application.authorize import AuthorizeDTO
from random_coffee.application.attach_person_to_telegram_account import AttachPersonToTelegramAccountDTO
from random_coffee.presentation.interactor_factory import (
    CoreInteractorFactory,
    TelegramInteractorFactory,
)
from random_coffee.presentation.telegram.states.authentication import (
    AuthenticationState
)


class NotAuthorized(Exception):
    pass


class AuthorizationMiddleware(BaseMiddleware):
    """Authorization middleware

    Checks if telegram account has enough credentials to enter selected
    handler.

    """

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]
            ],
            event: TelegramObject, data: Dict[str, Any]
    ) -> Any:
        core_ioc: CoreInteractorFactory = data.get('core_ioc')
        telegram_ioc: TelegramInteractorFactory = data.get('telegram_ioc')
        auth_state: FSMContext = cast(FSMContext, data.get('auth_state'))
        raw_auth_state: str = cast(str, data.get('raw_auth_state'))

        if not (access_scopes := flags.get_flag(
            cast(HandlerObject, handler), "access_scopes"
        )):
            access_scopes = set()

        if access_scopes and raw_auth_state != AuthenticationState.authenticated:
            raise RuntimeError(
                "Handlers that requires access scopes must also require "
                "authentication flow state `authenticated`."
            )
        if raw_auth_state != AuthenticationState.authenticated:
            return await handler(event, data)

        fsm_data = await auth_state.get_data()
        access_token = fsm_data.get('access_token')
        try:
            async with core_ioc.authorize() as use_case:
                response = await use_case(AuthorizeDTO(
                    access_token=access_token,
                    access_scopes=access_scopes,
                ))
        except AuthorizationError:
            await auth_state.set_state(AuthenticationState.not_authenticated)
            await auth_state.set_data(dict())
            return await event.bot.send_message(
                chat_id=auth_state.key.chat_id,
                text="Пожалуйста, войдите в аккаунт\n\n/login",
            )

        if not fsm_data.get("is_person_attached"):
            telegram_account = data.get('telegram_account')
            async with telegram_ioc.attach_person_to_telegram_account() as use_case:
                await use_case(AttachPersonToTelegramAccountDTO(
                    telegram_account_id=telegram_account.id,
                    person_id=response.account.person.id,
                ))
            await auth_state.update_data(is_person_attached=True)

        data.update({
            "authorization_response": response,
            "account": response.account,
            "person": response.account.person,
        })

        return await handler(event, data)
