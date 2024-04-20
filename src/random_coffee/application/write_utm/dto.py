from dataclasses import dataclass

from random_coffee.domain.core.models.utm import UTMId
from random_coffee.application.common.dto import UTMDTO


@dataclass
class WriteUTMDTO:
    utm_id: UTMId
    value: str


@dataclass
class WriteUTMResponseDTO:
    utm: UTMDTO
