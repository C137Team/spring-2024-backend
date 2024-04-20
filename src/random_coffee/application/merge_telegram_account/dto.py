from typing import Optional

from pydantic import BaseModel

from random_coffee.application.common.dto import TelegramAccountDTO


class MergeTelegramAccountDTO(BaseModel):
    telegram_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]


class MergeTelegramAccountResponseDTO(BaseModel):
    telegram_account: TelegramAccountDTO
