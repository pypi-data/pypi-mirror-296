import logging
from datetime import datetime

from pytz import timezone
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource

from no996.platform.config import settings

logging.Formatter.converter = lambda *args: datetime.now(
    tz=timezone(settings.TIME_ZONE)
).timetuple()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

taskiq_broker = AioPikaBroker(
    str(settings.AMQP_URI),
).with_result_backend(RedisAsyncResultBackend(str(settings.TASKIQ_BACKEND_URI)))


redis_source = RedisScheduleSource(str(settings.TASKIQ_BACKEND_URI))
scheduler = TaskiqScheduler(
    taskiq_broker, sources=[redis_source, LabelScheduleSource(taskiq_broker)]
)


@taskiq_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    # state.db_session = Session(engine)
    # logging.info("启动数据库连接")
    pass


@taskiq_broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    # state.db_session.commit()
    # state.db_session.close()
    # logging.info("关闭数据库连接")
    pass
