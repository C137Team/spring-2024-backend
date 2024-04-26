from random_coffee.domain.core.adapters import AllPersons
from random_coffee.domain.core.services import AuthenticationService

from random_coffee.application.login.dto import LoginDTO, LoginResponseDTO

from random_coffee.infrastructure.bases.use_case import UseCase
from random_coffee.infrastructure.security.token import create_access_token, CreateTokenData, Sub

from .dto import GetMyAchievementsDTO, GetMyAchievementsResponseDTO, achievements_to_dto
from ...domain.core.services.person_achievement import PersonAchievementService


class GetMyAchievements(UseCase[GetMyAchievementsDTO, GetMyAchievementsResponseDTO]):
    # noinspection PyProtocol
    def __init__(
            self,
            authentication_service: AuthenticationService,
            achievements_service: PersonAchievementService,
            all_persons: AllPersons,
    ):
        self.all_persons = all_persons
        self.achievements_service = achievements_service
        self.authentication_service = authentication_service

    async def __call__(self, payload: GetMyAchievementsDTO) -> GetMyAchievementsResponseDTO:
        person = await self.all_persons.with_id(
            payload.person_id,
        )

        achievements = await self.achievements_service.get_person_achievements(
            person=person,
            page=payload.page,
            limit=payload.limit
        )

        return GetMyAchievementsResponseDTO(
            achievements=achievements_to_dto(achievements),
        )
