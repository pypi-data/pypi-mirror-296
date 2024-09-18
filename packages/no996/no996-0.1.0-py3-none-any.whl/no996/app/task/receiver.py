from logging import getLogger
from typing import Union

from taskiq.abc.broker import AckableMessage
from taskiq.abc.middleware import TaskiqMiddleware
from taskiq.acks import AcknowledgeType
from taskiq.exceptions import NoResultError
from taskiq.receiver import Receiver
from taskiq.utils import maybe_awaitable

from .exception import TaskiqAckException

logger = getLogger(__name__)


class CustomerReceiver(Receiver):
    async def callback(  # noqa: C901, PLR0912
        self,
        message: Union[bytes, AckableMessage],
        raise_err: bool = False,
    ) -> None:
        """
        Receive new message and execute tasks.

        This method is used to process message,
        that came from brokers.

        :raises Exception: if raise_err is true,
            and exception were found while saving result.
        :param message: received message.
        :param raise_err: raise an error if cannot save result in
            result_backend.
        """
        message_data = message.data if isinstance(message, AckableMessage) else message
        try:
            taskiq_msg = self.broker.formatter.loads(message=message_data)
        except Exception as exc:
            logger.warning(
                "Cannot parse message: %s. Skipping execution.\n %s",
                message_data,
                exc,
                exc_info=True,
            )
            return
        logger.debug(f"Received message: {taskiq_msg}")
        task = self.broker.find_task(taskiq_msg.task_name)
        if task is None:
            logger.warning(
                'task "%s" is not found. Maybe you forgot to import it?',
                taskiq_msg.task_name,
            )
            return
        logger.debug(
            "Function for task %s is resolved. Executing...",
            taskiq_msg.task_name,
        )
        for middleware in self.broker.middlewares:
            if middleware.__class__.pre_execute != TaskiqMiddleware.pre_execute:
                try:
                    taskiq_msg = await maybe_awaitable(
                        middleware.pre_execute(
                            taskiq_msg,
                        ),
                    )
                except Exception as exc:
                    logger.exception(
                        "raise error from pre_execute: %s",
                        exc,
                        exc_info=True,
                    )
                    if isinstance(exc, TaskiqAckException):
                        await maybe_awaitable(message.ack())

        logger.info(
            "Executing task %s with ID: %s",
            taskiq_msg.task_name,
            taskiq_msg.task_id,
        )

        if self.ack_time == AcknowledgeType.WHEN_RECEIVED and isinstance(
            message,
            AckableMessage,
        ):
            await maybe_awaitable(message.ack())

        result = await self.run_task(
            target=task.original_func,
            message=taskiq_msg,
        )

        if self.ack_time == AcknowledgeType.WHEN_EXECUTED and isinstance(
            message,
            AckableMessage,
        ):
            await maybe_awaitable(message.ack())

        for middleware in self.broker.middlewares:
            if middleware.__class__.post_execute != TaskiqMiddleware.post_execute:
                await maybe_awaitable(middleware.post_execute(taskiq_msg, result))

        try:
            if not isinstance(result.error, NoResultError):
                await self.broker.result_backend.set_result(taskiq_msg.task_id, result)

                for middleware in self.broker.middlewares:
                    if middleware.__class__.post_save != TaskiqMiddleware.post_save:
                        await maybe_awaitable(middleware.post_save(taskiq_msg, result))

        except Exception as exc:
            logger.exception(
                "Can't set result in result backend. Cause: %s",
                exc,
                exc_info=True,
            )
            if raise_err:
                raise exc

        if self.ack_time == AcknowledgeType.WHEN_SAVED and isinstance(
            message,
            AckableMessage,
        ):
            await maybe_awaitable(message.ack())
