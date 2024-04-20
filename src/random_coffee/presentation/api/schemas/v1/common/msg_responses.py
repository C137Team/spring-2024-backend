from typing import Literal

from random_coffee.presentation.api.schemas.v1.base import NoContentResponse


class Ok(NoContentResponse):
    _status_code_: Literal[200]

    message: Literal['ok'] = 'ok'
