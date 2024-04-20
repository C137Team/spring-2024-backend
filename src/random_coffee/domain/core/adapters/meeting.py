from __future__ import annotations

from random_coffee.domain.core.models import Meeting
from random_coffee.infrastructure.repo import BaseEntityRepo


class AllMeetings(BaseEntityRepo[Meeting]):
    pass
