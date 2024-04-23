from typing import Literal

from random_coffee.domain.core.adapters import AllPersonsAchievements
from random_coffee.domain.core.adapters.notification_destination import \
    AllNotificationDestinations
from random_coffee.domain.core.adapters.person import AllPersons
from random_coffee.domain.core.services.notification import NotificationService
from random_coffee.infrastructure.security.scopes import AccessScopeEnum
from random_coffee.domain.core.exceptions.notification import (
    PersonHasNoNotificationDestinations,
    NotificationError,
    CantReportInternalError
)
from random_coffee.domain.core.models import Achievement, Person

from random_coffee.infrastructure.bases.service import BaseService


class PersonAchievementService(BaseService):
    def __init__(
            self,
            notification_service: NotificationService,
            all_persons_achievement: AllPersonsAchievements,
    ):
        self.notification_service = notification_service
        self.all_persons_achievement = all_persons_achievement

    async def give_achievement(
            self,
            achievement: Achievement,
            person: Person,
    ):
        await self.all_persons_achievement.create(
            achievement_id=achievement.id,
            person_id=person.id,
        )
        await self.notification_service.notify_person(
            person_id=person.id,
            notification_content=
            f"Вы получили ачивку {achievement.title}!"
        )

    async def get_person_achievmenets(
            self,
            person: Person,
    ):
        return await self.all_persons_achievement.with_person_id(
            person_id=person.id
        )
