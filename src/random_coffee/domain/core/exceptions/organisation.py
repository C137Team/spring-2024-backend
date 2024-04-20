from random_coffee.infrastructure.bases.domain_error import DomainError


class OrganisationServiceError(DomainError):
    pass


class EmployeeAlreadyExists(OrganisationServiceError):
    pass


class EmployeeDoesNotExists(OrganisationServiceError):
    pass
