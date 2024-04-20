from random_coffee.domain.core.adapters.account import AllAccounts
from random_coffee.infrastructure.security.password import verify_password, get_password_hash

from random_coffee.domain.core.models import Account, Person
from random_coffee.domain.core.exceptions.authentication import (
    AuthenticationError,
    LoginAlreadyOccupiedError,
)

from random_coffee.infrastructure.bases.service import BaseService


class AuthenticationService(BaseService):
    def __init__(
            self,
            all_accounts: AllAccounts,
    ):
        self.all_accounts = all_accounts

    async def register_account(
            self,
            email: str,
            password: str,
            person: Person,
    ) -> Account:
        """

        :param email:
        :param password:
        :param person:
        :raise LoginAlreadyOccupiedError
        :return:
        """
        is_login_occupied = await self.all_accounts.is_email_occupied(email)

        if is_login_occupied:
            raise LoginAlreadyOccupiedError()

        password_hash = get_password_hash(password)

        account = await self.all_accounts.create(
            email=email,
            password_hash=password_hash,
            person=person,
        )

        return account

    async def authenticate(
            self,
            login: str,
            password: str,
    ) -> Account:
        """

        :param login:
        :param password:
        :raise AuthenticationError:
        :return:
        """
        account = await self.all_accounts.get_by_login(login)

        if account is None:
            raise AuthenticationError()

        is_verified = verify_password(password, account.password_hash)

        if not is_verified:
            raise AuthenticationError()

        return account
