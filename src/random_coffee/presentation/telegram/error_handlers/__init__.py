from aiogram import Router

from . import (
    auth,
)


router = Router()


router.include_router(auth.router)
