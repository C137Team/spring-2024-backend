from typing import ClassVar, Union, Dict, Any, Optional

from aiogram.types import TelegramObject
from aiogram.filters.state import StateFilter as _StateFilter


class BaseStateFilter(_StateFilter):
    __raw_state_keyword__: ClassVar[str] = "raw_state"

    async def __call__(
            self, obj: TelegramObject, **data,
    ) -> Union[bool, Dict[str, Any]]:
        raw_state: Optional[str] = data.get(self.__raw_state_keyword__)
        result = await super().__call__(obj, raw_state)
        return result


class StateFilter(BaseStateFilter):
    __raw_state_keyword__ = "raw_state"  # `default` state destiny


class AuthenticationStateFilter(BaseStateFilter):
    __raw_state_keyword__ = "raw_auth_state"  # `auth` state destiny
