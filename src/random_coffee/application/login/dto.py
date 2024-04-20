from dataclasses import dataclass


@dataclass
class LoginDTO:
    login: str
    password: str
    security_scopes: list[str]


@dataclass
class LoginResponseDTO:
    access_token: str
