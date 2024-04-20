from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from random_coffee.infrastructure.value_object import BaseVO

from random_coffee.domain.core.models import Employee


@dataclass
class MatchingGroup:
    employees: list[Employee]
