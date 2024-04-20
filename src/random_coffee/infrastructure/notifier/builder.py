from random_coffee.infrastructure.config import Environment

from .interface import Notifier

from .backends import (
    TelegramNotifierBackend
)


def build_notifier(environment: Environment) -> Notifier:
    result = Notifier(
        [
            TelegramNotifierBackend(
                bot_token=environment.telegram_bot_token,
            ),
        ],
    )
    return result
