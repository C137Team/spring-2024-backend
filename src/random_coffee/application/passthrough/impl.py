from random_coffee.infrastructure.service import BaseService


class Passthrough(BaseService):
    """Passthrough

    This is temporary solution to pass domain object to the presentation
    layer, due lack of time.

    """
    def __init__(
            self,
    ):
        pass
