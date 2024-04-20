from dataclasses import dataclass

from random_coffee.domain.core.models.utm import UTMId
from random_coffee.application.common.dto import UTMDTO


@dataclass
class ReadUTMDTO:
    utm_id: UTMId


@dataclass
class ReadUTMResponseDTO:
    utm: UTMDTO
