from typing import Annotated, AbstractSet

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import SecurityScopes

from random_coffee.infrastructure.security.scopes import AccessScopeEnum
from random_coffee.domain.core import exceptions
from random_coffee.application.authorize import (
    AuthorizeDTO, AuthorizeResponseDTO
)
from random_coffee.application.common.dto import AccountDTO

from random_coffee.presentation.api.auth import oauth2_scheme

from .ioc import CoreIoCDep


def get_access_scopes(scopes: SecurityScopes) -> AbstractSet[AccessScopeEnum]:
    return set(map(AccessScopeEnum, scopes.scopes))


async def require_authorization(
        security_scopes: SecurityScopes,
        ioc: CoreIoCDep,
        token: Annotated[str, Depends(oauth2_scheme)] = ...,
) -> AuthorizeResponseDTO:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scopes="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    access_scopes = get_access_scopes(security_scopes)

    try:
        async with ioc.authorize() as use_case:
            response = await use_case(AuthorizeDTO(
                access_token=token,
                access_scopes=set(access_scopes),
            ))
    except exceptions.authorization.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value}
        )
    except exceptions.authorization.AuthorizationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value}
        )

    return response


async def get_current_account(
        authorization: Annotated[AuthorizeResponseDTO, Depends(require_authorization)],
) -> AccountDTO:
    return authorization.account


async def get_current_person(
        account: Annotated[AccountDTO, Depends(get_current_account)],
        security_scopes: SecurityScopes,
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scopes="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    if account.person is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not identified",
            headers={"WWW-Authenticate": authenticate_value}
        )

    return account.person
