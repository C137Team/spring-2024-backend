from typing import Annotated

from fastapi import APIRouter, Depends

from random_coffee.domain.core import models

from random_coffee.application.confirm_identification import (
    ConfirmIdentificationDTO,
    ConfirmIdentificationResponseDTO,
)

from random_coffee.infrastructure.dto import BaseDTO
from random_coffee.presentation.api import dependencies
from random_coffee.presentation.api.dependencies.ioc import CoreIoCDep


router = APIRouter(tags=["Me", "Identification"])


class IdentificationConfirmationSchemeDTO(BaseDTO):
    confirmation_code: str


@router.post(
    "/me/account/identification/confirm",
    response_model=ConfirmIdentificationResponseDTO,
)
async def create_identification_request(
        ioc: CoreIoCDep,
        current_account: Annotated[
            models.Account, Depends(dependencies.get_current.get_current_account)
        ],
        payload: IdentificationConfirmationSchemeDTO,
):

    async with ioc.confirm_identification() as use_case:
        result = await use_case(ConfirmIdentificationDTO(
            account_id=current_account.id,
            confirmation_code=payload.confirmation_code,
        ))
        return result
