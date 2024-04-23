from sqladmin import ModelView

from random_coffee.domain.core.models import Achievement


class AchievementAdmin(ModelView, model=Achievement):
    column_list = [
        Achievement.id,
        Achievement.title,
        Achievement.description,
        Achievement.image,
    ]
