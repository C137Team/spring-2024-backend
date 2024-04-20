from di.dependent import Injectable

from random_coffee.infrastructure.database import DatabaseSession


class BaseDbGateway(Injectable):
    """Base database gateway class

    Method naming conventions:
    * method names must contain full model name in the snake_case,
      to avoid name conflicts.
    * prefix `get` refers to operation, that must exactly return
      an object. if object not found, error will be raised
    * prefix `find` refers to `get` method, that returns None
      on error.
    * prefix `search` refers to method, that returns an iterable.

    """

    def __init__(self, session: DatabaseSession):
        self.session = session

    def __init_subclass__(cls, **kwargs):
        kwargs.setdefault('scope', 'request')
        return super().__init_subclass__(cls, **kwargs)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()

    async def save(
            self,
            obj,
    ):
        self.session.add(obj)
        await self.session.flush((obj,))

    async def save_all(
            self,
            objs,
    ):
        self.session.add_all(objs)
        await self.session.flush(objs)
