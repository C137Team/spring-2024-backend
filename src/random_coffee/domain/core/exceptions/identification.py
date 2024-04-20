from .base import DomainError


class IdentificationServiceError(DomainError):
    pass


class NoPendingIdentificationRequestsError(IdentificationServiceError):
    pass


class EmailNotBelongsToAnyOrganisation(IdentificationServiceError):
    pass


class IdentificationConfirmationNotVerified(IdentificationServiceError):
    pass
