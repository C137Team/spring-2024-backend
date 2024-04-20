from __future__ import annotations

from random_coffee.domain.core.models.administrator import Administrator
from random_coffee.domain.core.models.employee import Employee
from random_coffee.infrastructure.repo import BaseRepo, BaseEntityRepo


class AllAdministrators(BaseEntityRepo[Administrator]):
    pass
