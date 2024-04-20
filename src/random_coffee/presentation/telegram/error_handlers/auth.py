from aiogram import Router, types, F
from aiogram.filters import ExceptionTypeFilter

from random_coffee.presentation.telegram.errors.auth import AccountNotIdentifiedError


router = Router()


@router.error(
    ExceptionTypeFilter(AccountNotIdentifiedError),
    F.update.message.as_("message"),
)
async def auth_errors_handler(
        event: types.ErrorEvent,
        message: types.Message,
):
    await message.answer(
        "Бот пока не поддерживает взаимодействие с аккаунтами, которые"
        " не привязаны к определённому человеку в системе."
    )
