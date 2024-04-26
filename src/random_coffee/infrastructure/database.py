from typing import Annotated
from di.dependent import Injectable

from sqlalchemy import create_engine, BigInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs

from random_coffee.infrastructure.config import environment


def _create_engine(driver: str, is_async: bool):
    if is_async:
        create = create_async_engine
    else:
        create = create_engine

    print('postgresql+{}://{}:{}@{}:{}/{}'.format(
            driver,
            environment.postgres_user,
            environment.postgres_password,
            environment.postgres_host,
            environment.postgres_port,
            environment.postgres_db
        ))

    engine_ = create(
        'postgresql+{}://{}:{}@{}:{}/{}'.format(
            driver,
            environment.postgres_user,
            environment.postgres_password,
            environment.postgres_host,
            environment.postgres_port,
            environment.postgres_db
        ),
        echo=environment.sqlalchemy_echo,
    )

    return engine_


try:
    engine = _create_engine('psycopg', is_async=True)
except ImportError:
    engine = None

try:
    sync_engine = _create_engine('psycopg2', is_async=False)
except ImportError:
    sync_engine = None


async def inject_database_session():
    async with DatabaseSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()


# noinspection PyAbstractClass
class DatabaseSession(AsyncSession, Injectable, call=inject_database_session, scope='request'):
    pass


class RelationalMapper(DeclarativeBase, AsyncAttrs):
    pass


async def on_startup():
    async with engine.begin() as session:
        # await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(RelationalMapper.metadata.create_all)


TelegramIdentifier = Annotated[int, mapped_column(BigInteger())]
