from random_coffee.domain.core import models
from random_coffee.domain.core.adapters.administrator import AllAdministrators
from random_coffee.domain.core.adapters.employee import AllEmployees
from random_coffee.domain.core.adapters.organisation import AllOrganisations
from random_coffee.domain.core.exceptions.organisation import (
    EmployeeAlreadyExists,
    EmployeeDoesNotExists,
)

from random_coffee.infrastructure.bases.service import BaseService


class OrganisationService(BaseService):
    def __init__(
            self,
            all_organisations: AllOrganisations,
            all_employees: AllEmployees,
            all_administrators: AllAdministrators,
    ):
        self.all_organisations = all_organisations
        self.all_employees = all_employees
        self.all_administrators = all_administrators

    async def create_employee(
            self,
            person: models.Person,
            organisation_id: int,
    ) -> models.Employee:
        employee = await self.all_employees.with_value(
            person_id=person.id,
            organisation_id=organisation_id,
        )

        if employee is not None:
            raise EmployeeAlreadyExists()

        employee = await self.all_employees.create(
            person_id=person.id,
            organisation_id=organisation_id,
        )
        return employee

    async def remove_employee(
            self,
            person: models.Person,
            organisation: models.Organisation,
    ) -> None:
        employee = await self.all_employees.with_value(
            person_id=person.id,
            organisation_id=organisation.id,
        )
        if employee is None:
            raise EmployeeDoesNotExists()
        await self.all_employees.delete_by_id(employee.id)
        return None
