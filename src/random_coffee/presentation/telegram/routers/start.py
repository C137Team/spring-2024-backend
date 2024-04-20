from aiogram import Router, types
from aiogram.filters import CommandStart

from random_coffee.application.common.dto import PersonDTO
from random_coffee.infrastructure.aiogram.state_filter import (
    AuthenticationStateFilter,
)
from random_coffee.presentation.telegram.states import AuthenticationState


router = Router()


@router.message(
    AuthenticationStateFilter(AuthenticationState.not_authenticated),
    CommandStart(),
)
async def start_command_handler(
        message: types.Message,
        person: PersonDTO,
):
    await message.answer(
        "Приветсвую тебя, путник!"
    )


@router.message(
    AuthenticationStateFilter(AuthenticationState.authenticated),
    CommandStart(),
)
async def start_command_handler(
        message: types.Message,
):
    await message.answer(
        "Приветсвую тебя, путник! Где-то я тебя уже видел..."
    )
