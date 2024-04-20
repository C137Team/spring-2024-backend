from dataclasses import dataclass
from itertools import islice
from typing import AbstractSet

from random_coffee.domain.core.models import Meeting, Employee
from random_coffee.domain.core.models.matching_group import MatchingGroup
from random_coffee.infrastructure.service import BaseService


def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


@dataclass
class MatchingResult:
    planned_meetings: AbstractSet[Meeting]
    unmatched_employees: AbstractSet[Employee]


class MatchingStrategy(BaseService):
    async def __call__(
            self,
            matching_group: MatchingGroup,
    ) -> MatchingResult:
        raise NotImplementedError()


class MatchingStrategyFullyBatched(MatchingStrategy):
    async def __call__(
            self,
            matching_group: MatchingGroup,
    ) -> MatchingResult:
        employees = matching_group.employees.copy()
        if len(employees) <= 1:
            return MatchingResult(
                planned_meetings=set(),
                unmatched_employees=set(employees),
            )

        subgroups = [
            list(i) for i in batched(employees, 2)
        ]
        if len(subgroups[-1]) == 1:
            subgroups[-2] += subgroups[-1]

        planned_meetings = {
            Meeting(participants=i)
            for i in subgroups
        }
        return MatchingResult(
            planned_meetings=planned_meetings,
            unmatched_employees=set(),
        )
