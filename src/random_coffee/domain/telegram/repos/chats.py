from random_coffee.infrastructure.repo import BaseEntityRepo
from random_coffee.domain.telegram.models import Chat


class AllChats(BaseEntityRepo[Chat]):
    pass
