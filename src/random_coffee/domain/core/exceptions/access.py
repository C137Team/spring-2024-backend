from .base import DomainError


class AccessServiceError(DomainError):
    pass


class AccessDeniedError(AccessServiceError):
    pass
