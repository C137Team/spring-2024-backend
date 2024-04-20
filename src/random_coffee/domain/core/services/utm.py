from typing import Optional
from uuid import UUID
import datetime


from random_coffee.domain.core.models import UTM

from random_coffee.domain.core import exceptions, adapters

from random_coffee.infrastructure.service import BaseService


class UTMService(BaseService):
    def __init__(self,
                 all_utms: adapters.AllUTMs):

        self.all_utms = all_utms

    async def create_utm(
            self,
            value: Optional[str],
            expire_seconds: int,
            read_limit: int,
    ):
        expire_at = (datetime.datetime.now()
                     + datetime.timedelta(seconds=expire_seconds))
        obj = await self.all_utms.create(
            value=value,
            expire_at=expire_at,
            read_limit=read_limit,
        )
        return obj

    async def write_utm(
            self, utm_id: UUID,
            value: Optional[str],
    ) -> UTM:
        utm = await self.all_utms.with_id(utm_id)

        if utm is None:
            raise exceptions.utm.UTMNotFound()
        if utm.expire_at <= datetime.datetime.now():
            raise exceptions.utm.UTMExpired()

        utm.value = value
        await self.all_utms.save(utm)

        return utm

    async def read_utm(
            self,
            utm_id: UUID,
    ) -> UTM:
        utm = await self.all_utms.with_id(utm_id)

        if utm is None:
            raise exceptions.utm.UTMNotFound()
        if utm.expire_at <= datetime.datetime.now():
            raise exceptions.utm.UTMExpired()
        if utm.read_count >= utm.read_limit:
            raise exceptions.utm.UTMReachedReadLimit()

        utm.read_count += 1

        await self.all_utms.save(utm)

        return utm
