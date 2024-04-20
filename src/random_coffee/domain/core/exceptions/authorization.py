from .base import DomainError


class AuthorizationServiceError(DomainError):
    pass


class AuthorizationError(AuthorizationServiceError):
    pass


class InvalidCredentialsError(AuthorizationError):
    pass


class AccountNotIdentifiedError(AuthorizationServiceError):
    pass
