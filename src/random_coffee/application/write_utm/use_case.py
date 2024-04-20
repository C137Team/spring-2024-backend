from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.services import (
    UTMService,
)
from random_coffee.application.common.dto import (
    UTMDTO,
)

from .dto import WriteUTMDTO, WriteUTMResponseDTO


class WriteUTM(UseCase[WriteUTMDTO, WriteUTMResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            utm_service: UTMService,
    ):

        self.utm_service = utm_service

    async def __call__(
            self, payload: WriteUTMDTO
    ) -> WriteUTMResponseDTO:
        result = await self.utm_service.write_utm(
            utm_id=payload.utm_id,
            value=payload.value,
        )

        return WriteUTMResponseDTO(
            utm=await UTMDTO.from_model(result)
        )
