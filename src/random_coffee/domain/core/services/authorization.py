from typing import AbstractSet, Optional

from random_coffee.infrastructure.security.scopes import AccessScopeEnum

from random_coffee.domain.core.services.access import AccessService

from random_coffee.domain.core.models.account import Account
from random_coffee.domain.core.models.person import Person

from random_coffee.domain.core.exceptions import access as access_exceptions
from random_coffee.domain.core.exceptions.authorization import (
    AuthorizationError
)

from random_coffee.infrastructure.bases.service import BaseService


class AuthorizationService(BaseService):
    def __init__(
            self,
            access_service: AccessService,
    ):

        self.access_service = access_service

    async def authorize_account(
            self,
            account: Optional[Account],
            access_scopes: AbstractSet[AccessScopeEnum],
    ) -> None:
        """Authorize account method

        Ensure that specified account has required access scopes

        :param account:
        :param access_scopes:
        :raise InvalidTokenError:
        :raise AuthorizationError:
        :return:
        """

        if account is None:
            raise AuthorizationError()

        return None

    async def authorize_person(
            self,
            person: Person | None,
            access_scopes: AbstractSet[AccessScopeEnum],
    ) -> None:
        """Authorize person method

        Ensure that specified person has required access scopes.

        :param person:
        :param access_scopes:
        :raise AuthorizationError:
        :return:
        """

        if person is None:
            raise AuthorizationError()

        try:
            # await self.access_service.ensure_access(
            #     person_id=person.id,
            #     access_scope_keys=access_scopes
            # )
            return None
        except access_exceptions.AccessDeniedError:
            raise AuthorizationError()
