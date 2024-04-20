from dataclasses import dataclass
from pydantic import EmailStr

from random_coffee.application.common.dto import AccountDTO
from random_coffee.infrastructure.dto import BaseDTO


class RegisterDTO(BaseDTO):
    email: EmailStr
    password: str
    full_name: str


@dataclass
class RegisterResponseDTO:
    account: AccountDTO
