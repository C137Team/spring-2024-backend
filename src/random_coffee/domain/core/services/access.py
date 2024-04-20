from typing import Iterable, AbstractSet

from random_coffee.infrastructure.security.scopes import AccessScopeEnum

from ..exceptions.access import AccessDeniedError

from ..models.person import Person
from ..models.role import Role


from random_coffee.infrastructure.bases.service import BaseService


class AccessService(BaseService):
    def __init__(
            self,

    ):
        pass
