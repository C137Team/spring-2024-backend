from random_coffee.infrastructure.repo import BaseEntityRepo
from random_coffee.domain.telegram.models import File


class AllFiles(BaseEntityRepo[File]):
    pass
