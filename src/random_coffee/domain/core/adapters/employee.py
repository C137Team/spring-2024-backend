from __future__ import annotations

from sqlalchemy import select

from random_coffee.domain.core.models import Role
from random_coffee.domain.core.models.employee import Employee
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllEmployees(BaseEntityRepo[Employee]):
    async def create(
            self,
            person_id: int,
            organisation_id: int,
    ):
        obj = Employee(
            person_id=person_id,
            organisation_id=organisation_id,
        )
        await self.save(obj)

    async def with_value(
            self,
            person_id: int,
            organisation_id: int,
    ):
        stmt = (select(Employee)
                .where(Employee.person_id == person_id)
                .where(Employee.organisation_id == organisation_id))
        return await self.session.scalars(stmt)