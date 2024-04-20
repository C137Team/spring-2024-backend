from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from uuid import UUID

from random_coffee.infrastructure.uuid import is_valid_uuid
from random_coffee.application.read_utm import (
    ReadUTMDTO,
)
from random_coffee.domain.core import exceptions
from random_coffee.presentation.interactor_factory.core import CoreInteractorFactory


class UTMInterceptorOuterMiddleware(BaseMiddleware):
    """UTM interceptor outer middleware

    This middleware intercepts request payload, and checks, if it is an
    utm.  If it is, middleware fetches utm value and store it within
    `start_payload` (overrides raw payload).  But information about
    actual UTM steel available, it's stored within data with `utm` key.

    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        core_ioc: CoreInteractorFactory = data.get('core_ioc')
        payload = data.get('start_payload')
        if (
            not payload
            or not is_valid_uuid(payload)
        ):
            return await handler(event, data)

        utm_id = UUID(payload, version=4)

        async with core_ioc.read_utm() as use_case:
            try:
                response = await use_case(
                    ReadUTMDTO(
                        utm_id=utm_id,
                    )
                )
            except exceptions.utm.UTMError as e:
                return await handler(event, data)

        data.update({
            "utm": response.utm,
            "start_payload": response.utm.value,
        })

        return await handler(event, data)
