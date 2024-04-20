from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from random_coffee.presentation.interactor_factory.legacy import LegacyInteractorFactory
from random_coffee.presentation.interactor_factory.telegram import TelegramInteractorFactory
from random_coffee.presentation.interactor_factory.core import CoreInteractorFactory


class IoCInjectionMiddleware(BaseMiddleware):
    def __init__(self):
        self.core_ioc = CoreInteractorFactory()
        self.telegram_ioc = TelegramInteractorFactory()
        self.legacy_ioc = LegacyInteractorFactory()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        data.update({
            "core_ioc": self.core_ioc,
            "telegram_ioc": self.telegram_ioc,
            "legacy_ioc": self.legacy_ioc,
        })

        return await handler(event, data)


ioc_injection_middleware = IoCInjectionMiddleware()
