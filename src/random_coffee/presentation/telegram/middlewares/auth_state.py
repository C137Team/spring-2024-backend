from typing import Callable, Dict, Any, Awaitable, cast

from aiogram import Bot
from aiogram.types import TelegramObject
from aiogram.fsm.middleware import FSMContextMiddleware

from random_coffee.presentation.telegram.states.authentication import (
    AuthenticationState
)


class AuthenticationFSMContextOuterMiddleware(FSMContextMiddleware):
    """authentication finite state machine context outer middleware

    This middleware creates a generic FSMContext, that contains
    only information about user authentication. If compare
    implemented behavior with browser, that middleware injects
    storage that represents cookie files. But here, this storage
    is dedicated to use only for auth flow.

    Following values are injected here:
    * raw_auth_state
        String, that contains the authentication state
    * auth_fsm_storage
        Storage of the authentication state
    * auth_state
        FSMContext object, that refers to the authentication state

    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        bot: Bot = cast(Bot, data["bot"])
        context = self.resolve_event_context(bot, data, destiny="auth")
        data["auth_fsm_storage"] = self.storage
        if context:
            raw_auth_state = await context.get_state()
            if raw_auth_state is None:
                raw_auth_state = AuthenticationState.not_authenticated.state
                await context.set_state(raw_auth_state)
            data.update({"auth_state": context,
                         "raw_auth_state": await context.get_state()})
            async with self.events_isolation.lock(key=context.key):
                return await handler(event, data)
        else:
            return await handler(event, data)
