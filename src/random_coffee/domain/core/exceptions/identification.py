from .base import DomainError


class IdentificationServiceError(DomainError):
    pass


class NoPendingIdentificationRequestsError(IdentificationServiceError):
    pass


class UnknownEmailDomainError(IdentificationServiceError):
    pass


class IdentificationConfirmationNotVerified(IdentificationServiceError):
    pass
