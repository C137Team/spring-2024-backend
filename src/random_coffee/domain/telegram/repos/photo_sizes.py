from random_coffee.infrastructure.repo import BaseEntityRepo
from random_coffee.domain.telegram.models import PhotoSize


class AllPhotoSizes(BaseEntityRepo[PhotoSize]):
    pass
