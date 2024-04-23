from typing import Literal

from fastapi import status
from pydantic import BaseModel

from random_coffee.presentation.api.utils.schema_errors import HTTPExceptionWrapper


class Exceptions:
    class LoginAlreadyOccupiedError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_400_BAD_REQUEST
        __detail__ = 'login already occupied'


class Schemas:
    class LoginAlreadyOccupiedError(BaseModel):
        detail: Literal['login already occupied']
