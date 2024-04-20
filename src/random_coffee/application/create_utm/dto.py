from typing import Optional
from dataclasses import dataclass

from random_coffee.application.common.dto import UTMDTO


@dataclass
class CreateUTMDTO:
    value: Optional[str] = None
    expire_seconds: Optional[int] = None
    read_limit: Optional[int] = None


@dataclass
class CreateUTMResponseDTO:
    utm: UTMDTO
