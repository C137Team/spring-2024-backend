from __future__ import annotations
from typing import ClassVar, TypeVar, Callable, ParamSpec, Generic, AsyncContextManager, Optional
from functools import wraps
from contextlib import asynccontextmanager

from di import Container, SolvedDependent, ScopeState
from di.dependent import Dependent
from di.executors import AsyncExecutor

from config import Config, config


_RT = TypeVar("_RT")
_P = ParamSpec("_P")


WiredUseCase = AsyncContextManager[_RT]


class use_case_wrapper(Generic[_RT]):
    def __call__(self, fn: Callable[_P, _RT]) -> Callable[_P, WiredUseCase[_RT]]:
        @wraps(fn)
        @asynccontextmanager
        async def wrapper(interactor_factory: BaseInteractorFactory):
            solved = interactor_factory.get_solved(wrapper)
            async with (interactor_factory.container
                        .enter_scope(
                            scope='request',
                            state=interactor_factory.ioc_state,
                        )) as state:
                yield await solved.execute_async(
                    executor=interactor_factory.executor,
                    state=state,
                    values={
                        BaseInteractorFactory: interactor_factory,
                        Config: config,
                    },
                )

        wrapper.__is_use_case__ = True

        return wrapper


def is_use_case(fn):
    return getattr(fn, '__is_use_case__', False)


class BaseInteractorFactory:
    """Interactor factory base class

    Subclasses must implement interaction with application layer. This
    class provides automatically dependencies waring, based on `di`
    framework.

    This abstraction layer was implemented to use automatically
    waring for all the presentation modules. I don't know, for example,
    how provide direct support of the `di` module by FastAPI without
    fkn magic, so, this class simplifies `di` features to be used with
    other frameworks.

    """

    container: ClassVar[Container] = Container()
    __use_cases: ClassVar[dict] = None

    def __init_subclass__(cls, **kwargs):
        cls.container = Container()

    @classmethod
    def _ensure_use_cases(cls):
        if cls.__use_cases is None:
            cls.__use_cases = {
                fn: cls.container.solve(
                    dependency=Dependent(fn.__wrapped__, scope='request'),
                    scopes=['request'],
                )
                for fn in filter(is_use_case, vars(cls).copy().values())
            }

    def __init__(self):
        self._ensure_use_cases()

        self.executor = AsyncExecutor()
        self._ioc_state_context_manager = self.container.enter_scope('ioc')
        self.ioc_state: Optional[ScopeState] = None

    async def __aenter__(self):
        self.ioc_state = await self._ioc_state_context_manager.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        return await self._ioc_state_context_manager.__aexit__(*args, **kwargs)

    @classmethod
    def get_solved(cls, fn) -> SolvedDependent:
        return cls.__use_cases[fn]
