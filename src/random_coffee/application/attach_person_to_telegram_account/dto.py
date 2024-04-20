from dataclasses import dataclass


@dataclass
class AttachPersonToTelegramAccountDTO:
    telegram_account_id: int
    person_id: int


@dataclass
class AttachPersonToTelegramAccountResponseDTO:
    pass
