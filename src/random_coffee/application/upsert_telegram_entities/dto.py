from dataclasses import dataclass

import aiogram.types
from pydantic import EmailStr

from random_coffee.application.common.dto import AccountDTO
from random_coffee.infrastructure.dto import BaseDTO


class UpsertTelegramEntitiesDTO(BaseDTO):
    user: aiogram.types.User | None = None
    chat: aiogram.types.Chat | None = None


@dataclass
class UpsertTelegramEntitiesResponseDTO:
    pass
