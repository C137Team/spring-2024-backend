from aiogram.filters.state import StatesGroup, State


class AuthenticationState(StatesGroup):
    not_authenticated = State()
    authenticated = State()
