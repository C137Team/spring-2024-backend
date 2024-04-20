from typing import Protocol, TypeVar


PayloadType = TypeVar("PayloadType")
ResponseType = TypeVar("ResponseType")


class UseCase(Protocol[PayloadType, ResponseType]):
    async def __call__(self, payload: PayloadType) -> ResponseType:
        raise NotImplementedError()
