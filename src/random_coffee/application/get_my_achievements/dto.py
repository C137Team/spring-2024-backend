from dataclasses import dataclass


@dataclass
class GetMyAchievementsDTO:
    person_id: int


@dataclass
class GetMyAchievementsResponseDTO:
    achievements: list[AchievementDTO]
