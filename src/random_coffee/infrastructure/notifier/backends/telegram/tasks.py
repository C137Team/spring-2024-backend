import asyncio
import logging
from typing import Iterable

import celery
import celery.result
import celery.exceptions
from celery import shared_task, group

from random_coffee.infrastructure.dto import BaseDTO
from random_coffee.infrastructure.exceptions.notifier import NotifierBackendError
from aiogram import Bot, exceptions, types

from random_coffee.infrastructure.config import environment


logger = logging.getLogger(__name__)


class TelegramNotificationContentDTO(BaseDTO):
    from_chat_id: int | None = None
    message_id: int | None = None
    text: str | None = None
    entities: list[types.MessageEntity] | None = None
    reply_markup: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup | None = None


async def _execute(
        chat_id: int,
        content: TelegramNotificationContentDTO,
):
    bot = Bot(token=environment.telegram.bot.token)
    try:
        if content.message_id is not None and content.from_chat_id is not None:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=content.from_chat_id,
                message_id=content.message_id,
                reply_markup=content.reply_markup,
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=content.text,
                entities=content.entities,
                reply_markup=content.reply_markup,
            )
    finally:
        await bot.session.close()


@shared_task(default_retry_delay=45,  max_retries=10, rate_limit='10/s', bind=True)
def send_telegram_message_task(
        self: celery.Task,
        internal_destination_identifier: str,
        notification_content: str,
):
    notification_content = TelegramNotificationContentDTO.model_validate_json(notification_content)

    try:
        asyncio.run(_execute(
            chat_id=int(internal_destination_identifier),
            content=notification_content,
        ))
    except exceptions.TelegramForbiddenError as e:
        logger.debug(f"Message `{notification_content}` is not sent "
                     f"to telegram chat `{internal_destination_identifier}` "
                     f"due some irresistible telegram api error",
                     exc_info=e)
        return {"response": "forbidden", "chat_id": int(internal_destination_identifier)}
    except (exceptions.TelegramNetworkError, exceptions.TelegramRetryAfter, exceptions.TelegramServerError) as e:
        logger.warning("Retry due some temporary problem with telegram "
                       "server or my server network.",
                       exc_info=e)
        raise self.retry()
    except exceptions.TelegramAPIError as e:
        logger.error(f"Message `{notification_content}` is not sent "
                     f"to telegram chat `{internal_destination_identifier}` "
                     f"due some telegram api error. The same errors can lead to "
                     f"system down. Check if the bot token is valid and if server"
                     f" is connected to network",
                     exc_info=e)
        return {"response": "failure", "chat_id": int(internal_destination_identifier)}
    except Exception as e:
        logger.critical(f"Telegram notifier backend error", exc_info=e)
        raise NotifierBackendError() from e

    return {"response": "ok", "chat_id": int(internal_destination_identifier)}


@shared_task(bind=True, rate_limit='1/s')
def broadcast_telegram_message_task(
        self: celery.Task,
        internal_destination_identifiers: Iterable[str],
        notification_content: str,
        priority: int | None = None,
):
    content_sig = send_telegram_message_task.s(notification_content=notification_content)
    sig = group((content_sig.clone(kwargs=dict(internal_destination_identifier=i))
                 for i in internal_destination_identifiers))
    async_results_group = sig.apply_async(priotiry=priority)
    async_results_group.save()
    return {"response": "ok", "group_id": async_results_group.id}


@shared_task(rate_limit='1/s')
def fetch_telegram_notifications_stats(
        group_id: str,
):
    try:
        broadcast_celery_group: celery.result.GroupResult = celery.result.GroupResult.restore(group_id)
        result = {
            "statuses": dict(),
            "forbidden_chats_queue": [],
            "success_chats_queue": [],
        }
        result["statuses"].setdefault("pending", 0)

        def update_data_via_result(task_id, value):
            async_res = celery.result.AsyncResult(task_id)
            async_res.forget()
            if not isinstance(value, dict):
                return
            response = value["response"]
            result["statuses"].setdefault(response, 0)
            result["statuses"][response] += 1

            if response == 'forbidden':
                result["forbidden_chats_queue"].append(value['chat_id'])
            elif response == 'ok':
                result["success_chats_queue"].append(value['chat_id'])

            result["statuses"]["pending"] -= 1

        try:
            broadcast_celery_group.join_native(
                timeout=0.5,  # why freezes on one second???
                propagate=False,
                callback=update_data_via_result,
                no_ack=False,
            )
        except celery.exceptions.TimeoutError:
            pass

        return result
    except Exception as e:
        print('ERROR!!!')
        logger.exception(e)
