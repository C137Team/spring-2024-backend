from .base import DomainError


class AuthenticationServiceError(DomainError):
    pass


class AuthenticationError(AuthenticationServiceError):
    pass


class LoginAlreadyOccupiedError(AuthenticationServiceError):
    pass
