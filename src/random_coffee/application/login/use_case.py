from random_coffee.domain.core.services import AuthenticationService

from random_coffee.application.login.dto import LoginDTO, LoginResponseDTO

from random_coffee.infrastructure.bases.use_case import UseCase
from random_coffee.infrastructure.security.token import create_access_token, CreateTokenData, Sub


class Login(UseCase[LoginDTO, LoginResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            authentication_service: AuthenticationService,
    ):
        self.authentication_service = authentication_service

    async def __call__(self, payload: LoginDTO) -> LoginResponseDTO:
        await self.authentication_service.authenticate(
            login=payload.login,
            password=payload.password,
        )
        access_token = create_access_token(
            create_payload=CreateTokenData(
                sub=Sub(login=payload.login),
                scopes=payload.security_scopes,
            )
        )
        return LoginResponseDTO(
            access_token=access_token,
        )
