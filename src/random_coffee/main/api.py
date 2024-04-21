import locale
from datetime import datetime, timedelta

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqladmin import Admin
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from random_coffee.application.cleanup_wandering import CleanupWanderingDTO
from random_coffee.application.proceed_wander import ProceedWanderDTO
from random_coffee.domain.core.models.meeting_circumstances import \
    MeetingCircumstances
from random_coffee.domain.core.models.meeting_state import MeetingStateEnum
from random_coffee.infrastructure.database import engine, on_startup

from random_coffee.presentation.api.routers import v1
from random_coffee.presentation.api.admin import include_admin_views, auth_backend

from random_coffee.infrastructure.config import environment
from random_coffee.presentation.interactor_factory import CoreInteractorFactory

app = FastAPI(title="RKSI API")


authentication_backend = auth_backend.SQLAdminAuth(environment.jwt_secret)
admin_app = Admin(
    app,
    engine=engine,
    authentication_backend=authentication_backend,
)
include_admin_views(admin_app)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:3000",
]

if environment.allowed_origin:
    origins.append(environment.allowed_origin)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1.router)


async def prceed_wander():
    ioc = CoreInteractorFactory()
    async with ioc.proced_wander() as use_case:
        response = await use_case(ProceedWanderDTO(
            organisation_id=2,
        ))
    return response


async def cleanup_wandering():
    ioc = CoreInteractorFactory()
    async with ioc.cleanup_wandering() as use_case:
        response = await use_case(CleanupWanderingDTO(
            organisation_id=2,
        ))
    return response


async def update_meeting_statuses():
    ioc = CoreInteractorFactory()
    print('Process status update')
    async with ioc.passthrough() as ps:
        for i in await ps.all_meetings.all():
            circumstance: MeetingCircumstances = await i.awaitable_attrs.circumstances

            if i.state is MeetingStateEnum.SCHEDULED and circumstance.starts_at <= datetime.now():
                i.state = MeetingStateEnum.OCCUR

            if (i.state is MeetingStateEnum.OCCUR
                and circumstance.starts_at
                    + timedelta(minutes=circumstance.duration_m)
                    <= datetime.now()):
                i.state = MeetingStateEnum.COMPLETED

            await ps.all_meetings.save(i)


@app.on_event("startup")
async def on_application_startup():
    await on_startup()
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(prceed_wander, "interval", seconds=10)
    scheduler.add_job(cleanup_wandering, "interval", seconds=10)
    scheduler.add_job(update_meeting_statuses, "interval", seconds=5)
    scheduler.start()
    # scheduler.add_job()


def main():
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    if environment.application_protocol == 'HTTP':
        uvicorn.run(
            app=f'{__name__}:app',
            host="0.0.0.0",
            port=8000,
            reload=environment.application_autoreload,
            reload_dirs=['src'],
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
    elif environment.application_protocol == 'HTTPS':
        uvicorn.run(
            app=f'{__name__}:app',
            host="0.0.0.0",
            port=8000,
            ssl_certfile=environment.application_ssl_certfile,
            ssl_keyfile=environment.application_ssl_keyfile,
            reload=environment.application_autoreload,
            reload_dirs=['src'],
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
    else:
        raise KeyError(f"Unknown protocol `{environment.application_protocol}`")


if __name__ == "__main__":
    main()
