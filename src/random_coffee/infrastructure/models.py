from typing import Protocol, runtime_checkable, TYPE_CHECKING, Any

from datetime import datetime

from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import CoreSchema, core_schema
from pydantic.v1.validators import parse_datetime


class BuiltinSubtypeMixin:

    if TYPE_CHECKING:
        # assumes that implementation have one of init or new
        # implemented method
        def __init__(self, *args, **kwargs):
            pass

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls, handler(source_type.__base__)
        )


class DatetimeWithoutTimezone(datetime):
    @classmethod
    def __get_validators__(cls):
        yield lambda x, _: parse_datetime(x).replace(tzinfo=None)
