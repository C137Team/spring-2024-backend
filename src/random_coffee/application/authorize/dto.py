from dataclasses import dataclass

from random_coffee.infrastructure.security.scopes import AccessScopeEnum
from random_coffee.application.common.dto import AccountDTO


@dataclass
class AuthorizeDTO:
    access_token: str
    access_scopes: set[AccessScopeEnum]


@dataclass
class AuthorizeResponseDTO:
    account: AccountDTO
