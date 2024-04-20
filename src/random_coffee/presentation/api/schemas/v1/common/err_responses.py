from typing import Literal

from fastapi import status
from pydantic import BaseModel

from random_coffee.presentation.api.utils.schema_errors import HTTPExceptionWrapper


class Exceptions:
    class LoginAlreadyOccupiedError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_400_BAD_REQUEST
        __detail__ = 'login already occupied'

    class OrganisationNotFoundError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_404_NOT_FOUND
        __detail__ = 'organisation not found'

    class AmbiguousReferenceError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_400_BAD_REQUEST
        __detail__ = "ambiguous reference"

    class InvalidMentionSyntaxError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_400_BAD_REQUEST
        __detail__ = "invalid mention syntax"

    class EmptyReferenceError(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_404_NOT_FOUND
        __detail__ = "referenced entity not found"


class Schemas:
    class LoginAlreadyOccupiedError(BaseModel):
        detail: Literal['login already occupied']

    class OrganisationNotFoundError(BaseModel):
        detail: Literal['organisation not found']

    class AmbiguousReferenceError(BaseModel):
        detail: Literal['ambiguous reference']

    class InvalidMentionSyntaxError(BaseModel):
        detail: Literal['invalid mention syntax']

    class EmptyReferenceError(BaseModel):
        detail: Literal['referenced entity not found']
