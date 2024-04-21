from typing import Iterable

from sqlalchemy import select, delete

from random_coffee.domain.core.models import Employee
from random_coffee.domain.core.models.wandering_employee import (
    WanderingEmployee,
)

from random_coffee.infrastructure.repo import BaseEntityRepo


class AllWanderingEmployees(BaseEntityRepo[WanderingEmployee]):
    async def within_organisation(
            self,
            organisation_id: int,
    ) -> Iterable[WanderingEmployee]:
        stmt = (select(WanderingEmployee)
                .join(WanderingEmployee.employee)
                .where(Employee.organisation_id == organisation_id))
        return await self.session.scalars(stmt)

    async def with_employee_id(
            self,
            emplyee_id: int,
    ):
        stmt = (select(WanderingEmployee)
                .where(WanderingEmployee.employee_id == emplyee_id))
        return await self.session.scalar(stmt)

    async def delete_by_employee_id(
            self,
            emplyee_id: int,
    ):
        stmt = (delete(WanderingEmployee)
                .where(WanderingEmployee.employee_id == emplyee_id))
        await self.session.execute(stmt)
        return None
