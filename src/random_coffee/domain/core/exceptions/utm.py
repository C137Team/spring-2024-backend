from .base import DomainError


class UTMError(DomainError):
    pass


class UTMExpired(UTMError):
    pass


class UTMNotFound(UTMError):
    pass


class UTMReachedReadLimit(UTMError):
    pass
