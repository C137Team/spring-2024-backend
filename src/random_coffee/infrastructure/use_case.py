from typing import Generic, TypeVar

from di.dependent import Injectable


PayloadType = TypeVar("PayloadType")
ResponseType = TypeVar("ResponseType")


class UseCase(Injectable, Generic[PayloadType, ResponseType]):
    async def __call__(self, payload: PayloadType) -> ResponseType:
        raise NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        kwargs.setdefault('scope', 'request')
        return super().__init_subclass__(**kwargs)
