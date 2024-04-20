from typing import Annotated

from fastapi import APIRouter, Depends

from random_coffee.application.common.dto import PersonDTO, AccountDTO
from random_coffee.presentation.api import schemas, dependencies

router = APIRouter(tags=['Me'])


@router.get(
    '/me/person',
    response_model=PersonDTO,
)
async def get_me(
        person: Annotated[PersonDTO, Depends(dependencies.get_current.get_current_person)]
) -> PersonDTO:
    return person


@router.get(
    '/me/account',
    response_model=AccountDTO,
)
async def get_my_account(
        account: Annotated[AccountDTO, Depends(dependencies.get_current.get_current_account)]
):
    return account
