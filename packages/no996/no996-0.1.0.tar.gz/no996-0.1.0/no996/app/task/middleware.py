import logging
from collections.abc import Coroutine
from typing import Any

from sqlmodel import and_, insert, select, update
from taskiq.abc.middleware import TaskiqMiddleware
from taskiq.message import TaskiqMessage
from taskiq.result import TaskiqResult

from no996.platform.config import settings
from no996.platform.date import date_now
from app.enums import TaskStatus
from app.models import TaskRunner

from .exception import TaskiqAckException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingTaskMiddleware(TaskiqMiddleware):
    def __init__(self):
        super().__init__()
        self.allow_retry = False

    async def pre_execute(
        self,
        message: "TaskiqMessage",
    ) -> "TaskiqMessage | Coroutine[Any, Any, TaskiqMessage]":
        now = date_now(fmt=settings.DB_FMT)

        task_name = message.task_name
        task_name = task_name.split(":")[1]

        session = self.broker.state.session

        logger.info(f"[后台任务] 查看信息 message.label = {message.labels}")
        logger.info(f"[后台任务] self.allow_retry = {self.allow_retry}")
        if "schedule_type" in message.labels:
            if message.labels["schedule_type"] == "retry":
                self.allow_retry = True

        if not self.allow_retry:
            query = select(TaskRunner).where(
                and_(
                    TaskRunner.name == task_name,
                    TaskRunner.date == now,
                )
            )

            task_details = session.execute(query)
            task_details = task_details.scalars().first()

            if task_details:
                msg_dict = {
                    TaskStatus.RUNNING: "已经在运行中",
                    TaskStatus.ERROR: "运行次数超过阈值",
                    TaskStatus.FINISHED: "已处理完毕，无需执行！",
                }

                if task_details.status in (TaskStatus.RUNNING, TaskStatus.FINISHED):
                    msg = f"[后台任务] {msg_dict[task_details.status]} {message.task_id} ==> {message.task_name}"
                    logger.warning(msg)

                    result: TaskiqResult[Any] = TaskiqResult(
                        is_err=False,
                        log=None,
                        return_value=None,
                        execution_time=0.2,
                        error=None,
                        labels=message.labels,
                    )
                    await self.broker.result_backend.set_result(message.task_id, result)

                    logger.info("反馈成功")
                    logger.warning(
                        f"[后台任务] {message.task_id} ==> {message.task_name} "
                    )

                    raise TaskiqAckException(msg)

                elif task_details.status == TaskStatus.ERROR:
                    if task_details.run_num > 10:
                        msg = f"[后台任务] {msg_dict[task_details.status]} {message.task_id} ==> {message.task_name}"
                        logger.info(msg)
                        raise TaskiqAckException(msg)

                    __query = (
                        update(TaskRunner)
                        .where(and_(TaskRunner.taskid == task_details.taskid))
                        .values(
                            end_time=date_now(settings.DB_TIME_FMT),
                            run_num=TaskRunner.run_num + 1,
                            taskid=message.task_id,
                            status=TaskStatus.RUNNING,
                        )
                    )
                    session.execute(__query)

            else:
                __query = insert(TaskRunner).values(
                    {
                        "taskid": message.task_id,
                        "name": task_name,
                        "startup_time": date_now(settings.DB_TIME_FMT),
                        "date": now,
                        "run_num": 0,
                        "status": TaskStatus.RUNNING,
                    }
                )

                session.execute(__query)

            session.commit()

        return super().pre_send(message)

    async def post_save(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
    ) -> "None | Coroutine[Any, Any, None]":
        if not self.allow_retry:
            session = self.broker.state.session

            query = (
                update(TaskRunner)
                .where(and_(TaskRunner.taskid == message.task_id))
                .values(
                    end_time=date_now(settings.DB_TIME_FMT),
                    execution_time=result.execution_time,
                    status=(
                        TaskStatus.FINISHED if not result.is_err else TaskStatus.ERROR
                    ),
                )
            )
            session.execute(query)
            session.commit()
            logger.info(f"[后台任务] {message.task_name} 处理完毕！")
            logger.info("[后台任务] 关闭数据库连接")
        return super().post_save(message, result)

    def on_error(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
        exception: BaseException,
    ) -> Coroutine[Any, Any, None] | None:
        logger.info("错误信息" + str(exception))
        return super().on_error(message, result, exception)
