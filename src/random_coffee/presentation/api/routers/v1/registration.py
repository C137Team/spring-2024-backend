from fastapi import APIRouter

from random_coffee import application
from random_coffee.domain.core import exceptions

from random_coffee.presentation.api import schemas
from random_coffee.presentation.api.dependencies.ioc import CoreIoCDep

router = APIRouter(tags=['Auth'])


@router.post(
    '/register',
    response_model=application.register.RegisterResponseDTO,
    responses={
        400: {"model": schemas.v1.common.err_responses.Schemas.LoginAlreadyOccupiedError}
    }
)
async def register(
        ioc: CoreIoCDep,
        payload: application.register.RegisterDTO,
):
    async with ioc.register() as use_case:
        try:
            result = await use_case(
                payload,
            )
        except exceptions.authentication.LoginAlreadyOccupiedError:
            raise schemas.v1.common.err_responses.Exceptions.LoginAlreadyOccupiedError()

        return result
