from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.services import (
    UTMService,
)
from random_coffee.application.common.dto import (
    UTMDTO,
)

from .dto import ReadUTMDTO, ReadUTMResponseDTO


class ReadUTM(UseCase[ReadUTMDTO, ReadUTMResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            utm_service: UTMService,
    ):

        self.utm_service = utm_service

    async def __call__(
            self, payload: ReadUTMDTO
    ) -> ReadUTMResponseDTO:
        result = await self.utm_service.read_utm(
            utm_id=payload.utm_id,
        )

        return ReadUTMResponseDTO(
            utm=await UTMDTO.from_model(result)
        )
