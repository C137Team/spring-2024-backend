from dataclasses import dataclass

from random_coffee.application.common.dto import PersonDTO


@dataclass
class LoginDTO:
    login: str
    password: str
    security_scopes: list[str]


@dataclass
class LoginResponseDTO:
    access_token: str
    person: PersonDTO | None
