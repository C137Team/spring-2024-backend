from dataclasses import dataclass

from random_coffee.domain.core.models.person.achievement import Achievement


@dataclass
class GetMyAchievementsDTO:
    person_id: int
    limit: int
    page: int


@dataclass
class AchievementDTO:
    id: int
    type: str
    title: str
    description: str
    image: str


@dataclass
class GetMyAchievementsResponseDTO:
    achievements: list[AchievementDTO]


def achievement_to_dto(achievement: Achievement):
    return AchievementDTO(
        id=achievement.id,
        type=achievement.type,
        title=achievement.title,
        description=achievement.description,
        image=achievement.image
    )


def achievements_to_dto(achievements: list[Achievement]):
    return map(achievement_to_dto, achievements)
