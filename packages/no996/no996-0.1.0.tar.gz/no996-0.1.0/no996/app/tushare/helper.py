import functools
import json
import logging
import re
from collections.abc import Callable

import pandas as pd
import tenacity
import tushare as ts
from sqlmodel import String, and_, col
from sqlmodel import func as sqlfunc

from no996.platform.config import settings
from no996.platform.date import date_cal, date_now, date_range, get_last_date_or_today
from no996.platform.db import ActiveRecordMixin, SymbolActiveRecordMixin
from app.model.task_runner import TaskStatus
from app.repository.task_runner import TaskRunner, TaskRunnerRepository
from app.repository.tushare_core import TushareUserRepository

logger = logging.getLogger(__name__)


class TushareRetry:
    """
    本模块为 retry 充实函数，防止在 tushare 调用过程中出现网络错误。
    统一管理重复调用次数，防止出现无限循环。
    支持调用函数A时候，当任务为处理中的时候，能够排除同一个函数A的调用。
    支持下载的数据日期，能够统一规范格式化，支持清洗日期等。
    """

    def __init__(
        self,
        repository: type[SymbolActiveRecordMixin] | type[ActiveRecordMixin],
        score: int,
    ):
        # TODO 增加函数参数检查 tushare_check 检查是否到期
        self.repository_quote = repository
        self.repository = None
        self.score = score

        self.pro_api = ts.pro_api(settings.TUSHARE_TOKEN)

        self.func = None
        self.func_name = ""
        self.args = None
        self.kwargs = None
        self.doc = ""

        self.result_is_empty = False
        self.db_session = None

    def wrap_func_meta(self, func: Callable, args: tuple[any], kwargs: dict[any, any]):
        """
        加载函数元数据
        """
        self.func = func
        # 获取函数名称
        self.func_name = func.__name__
        self.args = args
        self.kwargs = kwargs
        self.doc = func.__doc__.strip()

    def check_score(self):
        """
        检查积分是否足够
        """
        run_able = settings.TUSHARE_SCORE >= self.score
        if not run_able:
            logger.warning(
                f"[{self.__class__.__name__}]暂时无法执行的函数：{self.doc}[{self.func_name}]，当前积分 {self.score} 积分不足。"
            )
        return settings.TUSHARE_SCORE >= self.score

    def check_task(
        self, params: dict | None = None, task_status: TaskStatus = TaskStatus.RUNNING
    ):
        """
        检查任务是否正在处理中
        """
        # 查询今天的任务状态
        created_at = date_now(settings.DB_FMT)

        statement = sqlfunc.cast(TaskRunner.created_at, String).like(f"%{created_at}%")
        statement = and_(
            statement,
            TaskRunner.status == task_status,
            TaskRunner.name == self.func_name,
        )

        if params:
            statement = and_(
                statement, sqlfunc.cast(TaskRunner.params, String) == json.dumps(params)
            )

        order_by = col(TaskRunner.created_at).desc()

        task_runner_repository = TaskRunnerRepository(self.db_session)
        task_runner = task_runner_repository.first_by_fields(
            statement, order_by=order_by
        )

        if task_runner:
            return True

        return False

    def check_task_status(self, params: dict | None = None):
        # 判断是否存在正在运行的任务
        exist_running_task = self.check_task(params=None)

        if exist_running_task:
            logger.warning(
                f"[{self.__class__.__name__}]任务[{self.func_name}] 正在处理中，无需重复执行"
            )
            return False

        # 判断是否存在已经执行的任务
        exist_success_task = self.check_task(params, TaskStatus.SUCCESS)
        if exist_success_task:
            logger.warning(
                f"[{self.__class__.__name__}]任务[{self.func_name}] 已经执行成功，无需重复执行"
            )
            return False

        # 判断是否存在结束的任务
        exist_finished_task = self.check_task(params, TaskStatus.FINISHED)
        if exist_finished_task:
            logger.warning(
                f"[{self.__class__.__name__}]任务[{self.func_name}] 已经执行结束，无需重复执行"
            )
            return False

        return True

    @staticmethod
    def format_pd_date(df: pd.DataFrame):
        # 正则表达式匹配以"date"结尾的列
        date_columns = [_col for _col in df.columns if re.search(r"date$", _col)]

        for _col in date_columns:
            df.loc[:, _col] = (
                df[_col]
                .infer_objects(copy=False)
                .fillna(value=settings.TUSHARE_MAX_DEFAULT_DATE)
            )

            df.loc[:, _col] = pd.to_datetime(df[_col], errors="coerce")

            # 循环所有列，将以"date"结尾的列转换为日期格式字符串
            df.loc[:, _col] = df[_col].apply(lambda x: x.strftime(settings.DB_FMT2))

    def remove_duplicate(self, df: pd.DataFrame):
        # 去除重复数据
        primary_key_list = self.repository.get_pk_column()
        df = df[~df.duplicated(subset=primary_key_list, keep="last")]
        return df

    def pre_start(self):
        tushare_user_repository = TushareUserRepository(self.db_session)
        is_valid = tushare_user_repository.is_valid(settings.TUSHARE_TOKEN)
        return is_valid

    def pre_execute(
        self, func: Callable, args: tuple[any], kwargs: dict[any, any]
    ) -> bool:
        """
        执行前处理，加载函数元数据，检查积分是否足够
        """
        try:
            is_score_enough = self.check_score()
            return is_score_enough
        except Exception as e:
            logging.error(f"[{self.__class__.__name__}]: {e}")
            return False

    @tenacity.retry(
        wait=tenacity.wait_random(min=20, max=60), stop=tenacity.stop_after_attempt(10)
    )
    def execute(self) -> pd.DataFrame:
        # 清理参数
        ready_remove_keys = ["context", "db_session", "__context", "__db_session"]
        for args_key in ready_remove_keys:
            if args_key in self.kwargs:
                del self.kwargs[args_key]

        f = getattr(self.pro_api, self.func.__name__)
        logger.info(self.kwargs)
        df = f(**self.kwargs)
        logger.info(df)
        return df

    def post_execute(self, df: pd.DataFrame):
        """
        执行后处理
        """
        self.result_is_empty = df.empty
        if df.empty:
            logging.warning(
                f"[{self.__class__.__name__}]: 函数名称：{self.func_name} [{self.kwargs}]的数据为空，"
            )
            return None

        df = self.remove_duplicate(df)
        self.format_pd_date(df)
        self.repository.df_to_sqlmodel(df)

    def run(self, func: Callable, args: tuple[any], kwargs: dict[any, any]):
        if self.pre_execute(func, args, kwargs):
            df = self.execute()
            self.post_execute(df)
            return True
        else:
            logger.error(f"[{self.__class__.__name__}] 积分不足，请充值")
            return False

    def create_task_runner_record(self, params: dict | None) -> TaskRunner:
        # 创建任务
        task_runner_repository = TaskRunnerRepository(self.db_session)
        task_runner_obj = task_runner_repository.create(
            {"name": self.func_name, "params": params, "status": TaskStatus.RUNNING}
        )

        logger.info(
            f"[{self.__class__.__name__}] 任务 {task_runner_obj.id}: [{task_runner_obj}] 开始执行"
        )
        return task_runner_obj

    def update_task_runner_record(
        self, task_runner: TaskRunner, task_status: TaskStatus
    ):
        task_runner.status = TaskStatus.SUCCESS
        task_runner_repository = TaskRunnerRepository(self.db_session)
        task_runner_repository.update(
            {"status": task_status, "updated_at": date_now().datetime},
            where_dict={"id": task_runner.id},
        )

    def retry_enum(self, field: str, value_list: list):
        def __inner(func):
            @functools.wraps(func)
            def __wrapper(*args, **kwargs):
                self.wrap_func_meta(func, args, kwargs)

                db_session = kwargs.get("db_session") or kwargs.get("__db_session")
                self.db_session = db_session

                params = {"field": field, "value_list": value_list}

                if not self.pre_start():
                    logger.error(f"[{self.__class__.__name__}]非法token，无法执行")
                    return

                if not self.check_task_status(params):
                    return

                task_runner_obj = self.create_task_runner_record(params)

                # 清理库表内数据
                self.repository = self.repository_quote(session=self.db_session)
                self.repository.delete()

                try:
                    for value in value_list:
                        kwargs[field] = value
                        run_status = self.run(func, args, kwargs)

                        msg = f"[{self.__class__.__name__}] 函数 {func.__name__} 的枚举值 {value}"

                        if run_status:
                            logger.info(f"{msg} 运行成功")

                            if self.result_is_empty:
                                logger.info(f"{msg} 数据为空")
                        else:
                            logger.info(f"{msg} 运行终止")
                except Exception as e:
                    logger.error(f"{self.func_name} 运行异常：{e}")
                    self.update_task_runner_record(
                        task_runner=task_runner_obj, task_status=TaskStatus.ERROR
                    )
                    raise e

                self.update_task_runner_record(
                    task_runner=task_runner_obj, task_status=TaskStatus.SUCCESS
                )

            return __wrapper

        return __inner

    def retry_date(
        self,
        date_field: str,
        date_source: str = "",
        start_date: str = "19910101",
    ):
        def __inner(func):
            @functools.wraps(func)
            def __wrapper(*args, **kwargs):
                self.wrap_func_meta(func, args, kwargs)

                db_session = kwargs.get("db_session") or kwargs.get("__db_session")
                self.db_session = db_session

                if not self.pre_start():
                    logger.warning(f"[{self.__class__.__name__}]非法token，无法执行")
                    return False

                self.repository = self.repository_quote(session=self.db_session)
                max_date = self.repository.max_field(date_field)

                if not max_date:
                    max_date = start_date
                else:
                    max_date = date_cal(max_date, days=1, fmt=settings.TUSHARE_FMT)

                task_runner_repository = TaskRunnerRepository(self.db_session)
                statement = and_(
                    TaskRunner.name == self.func_name,
                    col(TaskRunner.status).in_(
                        [TaskStatus.SUCCESS, TaskStatus.FINISHED]
                    ),
                )
                order_by = col(TaskRunner.created_at).desc()
                task_runner: TaskRunner = task_runner_repository.first_by_fields(
                    statement, order_by
                )

                if task_runner:
                    # 跑历史数据场景：
                    # 如果获取到，一般是1231 日期，然后进行日期天数 + 1，得到最终日期
                    # 变成第二年的 1月1日

                    # 跑每日数据场景
                    # 比如上一次跑查到的是5月6日，则会加1天，变成5月7日

                    runner_end_date = task_runner.params["end_date"]
                    runner_next_end_date = date_cal(
                        runner_end_date, days=1, fmt=settings.TUSHARE_FMT
                    )
                    last_date = get_last_date_or_today(
                        runner_next_end_date, fmt=settings.TUSHARE_FMT
                    )

                else:
                    # 第一次跑，直接获取最后一天
                    last_date = get_last_date_or_today(
                        max_date, fmt=settings.TUSHARE_FMT
                    )

                params = {"start_date": max_date, "end_date": last_date}

                if not self.check_task_status(params):
                    return None

                task_runner_obj = self.create_task_runner_record(params)

                date_list = date_range(
                    max_date,
                    last_date,
                    fmt=settings.TUSHARE_FMT,
                )

                try:
                    for date in date_list:
                        kwargs[date_field] = date
                        self.run(func, args, kwargs)
                except Exception as e:
                    logger.error(f"{self.func_name} 运行异常：{e}")
                    self.update_task_runner_record(
                        task_runner=task_runner_obj, task_status=TaskStatus.ERROR
                    )
                    raise e

                self.update_task_runner_record(
                    task_runner=task_runner_obj, task_status=TaskStatus.SUCCESS
                )

            return __wrapper

        return __inner

    def retry_symbol(
        self, start_date: str = "19910101", max_days=0, code_field="ts_code"
    ):
        def __inner(func):
            @functools.wraps(func)
            def __wrapper(*args, **kwargs):
                self.wrap_func_meta(func, args, kwargs)

                db_session = kwargs.get("db_session") or kwargs.get("__db_session")
                self.db_session = db_session

                if not self.pre_start():
                    logger.warning(f"[{self.__class__.__name__}]非法token，无法执行")
                    return False

                self.repository = self.repository_quote(session=self.db_session)
                symbol_obj_list = self.repository.select_symbols()

                for index, symbol_obj in enumerate(symbol_obj_list, 0):
                    # index_basic 表也叫 ts_code
                    symbol = symbol_obj.ts_code

                    max_trade_date = self.repository.select_max_trade_date_by_symbol(
                        symbol
                    )

                    if not max_trade_date:
                        task_runner_repository = TaskRunnerRepository(self.db_session)
                        __task_runner = task_runner_repository.search_params_by_name(
                            symbol
                        )
                        if __task_runner:
                            max_trade_date = __task_runner.params["end_date"]
                            logger.info(f"[helpers] {symbol} -> {max_trade_date}")
                            max_trade_date = date_cal(
                                max_trade_date, days=1, fmt=settings.TUSHARE_FMT
                            )
                        else:
                            max_trade_date = start_date
                            if self.func_name == "index_weight":
                                max_trade_date = symbol_obj.list_date.replace("-", "")
                                logger.info(
                                    f"[helpers] {symbol} 初始化日期 -> {max_trade_date}"
                                )
                                # 如果是90年代的 我直接用默认开始日期吧
                                if max_trade_date.startswith("199"):
                                    max_trade_date = start_date

                    else:
                        max_trade_date = date_cal(
                            max_trade_date, days=1, fmt=settings.TUSHARE_FMT
                        )

                    today = date_now(fmt=settings.TUSHARE_FMT)
                    last_date = date_cal(
                        max_trade_date, days=max_days, fmt=settings.TUSHARE_FMT
                    )

                    if max_trade_date > today:
                        max_trade_date = today

                    if last_date > today:
                        last_date = today

                    params = {
                        code_field: symbol,
                        "start_date": max_trade_date,
                        "end_date": last_date,
                    }

                    logger.info(
                        f"开始获取第{index +1} 个 代码为 [{symbol}] 的 [{max_trade_date}] ~ [{last_date}] 的历史数据"
                    )

                    if not self.check_task_status(params):
                        continue

                    task_runner_obj = self.create_task_runner_record(params)

                    try:
                        kwargs.update(params)
                        self.run(func, args, kwargs)
                    except Exception as e:
                        logger.error(f"{self.func_name} 运行异常：{e}")
                        self.update_task_runner_record(
                            task_runner=task_runner_obj, task_status=TaskStatus.ERROR
                        )
                        raise e

                    self.update_task_runner_record(
                        task_runner=task_runner_obj, task_status=TaskStatus.SUCCESS
                    )

                return

            return __wrapper

        return __inner
