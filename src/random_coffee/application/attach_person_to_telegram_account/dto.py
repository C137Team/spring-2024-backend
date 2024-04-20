from dataclasses import dataclass


@dataclass
class AttachPersonToTelegramAccountDTO:
    telegram_account_id: int
    person_secret: str


@dataclass
class AttachPersonToTelegramAccountResponseDTO:
    access_token: str
