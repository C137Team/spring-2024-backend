from typing import Annotated, TypeAlias

from fastapi import Depends

from random_coffee.presentation.interactor_factory.core import CoreInteractorFactory


async def get_ioc() -> CoreInteractorFactory:
    yield CoreInteractorFactory()


CoreIoCDep: TypeAlias = Annotated[CoreInteractorFactory, Depends(get_ioc)]
