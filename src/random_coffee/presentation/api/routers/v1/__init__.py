from fastapi import APIRouter

from . import (
    token,
    telegram,
    registration,
    me,
    identification,
    utm,
)

router = APIRouter(prefix='/v1')

router.include_router(token.router)
router.include_router(telegram.router)
router.include_router(registration.router)
router.include_router(me.router)
router.include_router(identification.router)
router.include_router(utm.router)
