from random_coffee.application.confirm_identification.dto import (
    ConfirmIdentificationDTO,
    ConfirmIdentificationResponseDTO,
)
from random_coffee.domain.core.exceptions.authorization import (
    InvalidCredentialsError,
)
from random_coffee.domain.telegram.repos import AllAccounts
from random_coffee.infrastructure.security.token import decode_access_token, \
    InvalidCredentialsError as SubdomainInvalidCredentialsError
from random_coffee.infrastructure.bases.use_case import UseCase

from random_coffee.domain.core.services import (
    AuthorizationService, AuthenticationService,
    IdentificationService,
)

from random_coffee.application.common.dto import PersonDTO


class ConfirmIdentification(
    UseCase[ConfirmIdentificationDTO, ConfirmIdentificationResponseDTO],
):
    # noinspection PyProtocol
    def __init__(
            self,
            authorization_service: AuthorizationService,
            all_accounts: AllAccounts,
            authentication_service: AuthenticationService,
            identification_service: IdentificationService,
    ):
        self.authorization_service = authorization_service
        self.all_accounts = all_accounts
        self.authentication_service = authentication_service
        self.identification_service = identification_service

    async def __call__(
            self, payload: ConfirmIdentificationDTO
    ) -> ConfirmIdentificationResponseDTO:
        account = await self.all_accounts.with_id(payload.account_id)

        person = await self.identification_service.confirm_identification(
            account=account,
            confirmation_code=payload.confirmation_code,
        )
        return ConfirmIdentificationResponseDTO(
            person=await PersonDTO.from_model(person)
        )
