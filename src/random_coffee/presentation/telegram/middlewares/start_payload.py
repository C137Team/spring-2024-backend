from typing import Callable, Dict, Any, Awaitable

import re

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.utils import deep_linking


class StartPayloadOuterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject, data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        if event.text is None or not re.match(
                r'^/start .*$', event.text
        ):
            return await handler(event, data)

        payload = event.text.split()[1]
        data.update({
            "start_payload": payload,
        })
        return await handler(event, data)
