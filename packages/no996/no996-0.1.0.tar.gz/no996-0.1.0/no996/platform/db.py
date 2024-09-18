import logging
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.pool import QueuePool
from sqlmodel import (
    Session,
    SQLModel,
    String,
    and_,
    col,
    create_engine,
    delete,
    func,
    select,
)
from sqlmodel.sql.expression import ColumnElement, SelectOfScalar

from app import crud
from no996.platform.config import settings
from no996.platform.date import date_now, timer_decorator
from no996.platform.indicators import IndicatorsConfigMixin
from app.models import User, UserCreate

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_timeout=30,
    pool_recycle=3600,
    poolclass=QueuePool,
)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28

DATA_ROOT = Path("app/data")
DATA_JSON_PATH = (DATA_ROOT / "task_schedule.json").resolve()


def init_db(session: Session) -> User:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from no996.platform.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    return user


class ActiveRecordMixin:
    def __init__(self, model: type[SQLModel], session: Session):
        self.model = model
        self.session = session

    def get_model(self) -> type[SQLModel]:
        return self.model

    def get_pk_column(self) -> [str]:
        primary_key_list = []
        for name, column in self.model.model_fields.items():
            if not hasattr(column, "primary_key"):
                return
            primary_key_status = column.primary_key
            if isinstance(primary_key_status, bool) and primary_key_status:
                primary_key_list.append(name)
        return primary_key_list

    @staticmethod
    def compile(statement: ColumnElement | SelectOfScalar):
        # 编译SQL查询语句，获取编译结果
        # compiled = statement.compile()
        #
        # # 获取参数化的值
        # params = compiled.params
        #
        # logging.info(f"SQL: {compiled}")
        # logging.info(f"Params: {params}")
        pass

    def first(self):
        statement = select(self.model)
        return self.session.exec(statement).first()

    def max_field(self, field: str):
        statement = select(func.max(getattr(self.model, field)))
        self.compile(statement)
        return self.session.exec(statement).first()

    def one_by_id(self, _id: int):
        obj = self.session.get(self.model, _id)
        return obj

    def first_by_field(self, field: str, value: Any):
        return self.first_by_fields({field: value})

    def one_by_field(self, field: str, value: Any):
        return self.one_by_fields({field: value})

    def first_by_fields(
        self,
        where_statement: dict | ColumnElement,
        order_by: ColumnElement | None = None,
    ):
        statement = select(self.model)

        if isinstance(where_statement, ColumnElement):
            statement = statement.where(where_statement)
        else:
            for key, value in where_statement.items():
                statement = statement.where(getattr(self.model, key) == value)

        if order_by is not None:
            statement = statement.order_by(order_by)
        self.compile(statement)
        return self.session.exec(statement).first()

    def one_by_fields(self, fields: dict):
        statement = select(self.model)
        for key, value in fields.items():
            statement = statement.where(getattr(self.model, key) == value)
        try:
            return self.session.exec(statement).one()
        except NoResultFound:
            logging.error(f"{self.model}: one_by_fields failed, NoResultFound")
            return None

    def all_by_field(self, field: str, value: Any):
        statement = select(self.model).where(getattr(self.model, field) == value)
        return self.session.exec(statement).all()

    def all_by_fields(
        self,
        where_statement: dict | ColumnElement | None = None,
        order_by: ColumnElement | None = None,
    ):
        statement = select(self.model)

        if where_statement is not None:
            if isinstance(where_statement, ColumnElement):
                statement = statement.where(where_statement)
            else:
                for key, value in where_statement.items():
                    statement = statement.where(getattr(self.model, key) == value)

        if order_by is not None:
            statement = statement.order_by(order_by)

        self.compile(statement)
        return self.session.exec(statement).all()

    def convert_without_saving(
        self, source: dict | SQLModel, update: dict | None = None
    ) -> SQLModel:
        obj = None
        if isinstance(source, SQLModel):
            obj = self.model.from_orm(source, update=update)
        elif isinstance(source, dict):
            obj = self.model.model_validate(source, update=update)
        return obj

    def create(self, source: dict | SQLModel, update: dict | None = None):
        obj = self.convert_without_saving(source, update)
        if obj is None:
            return None
        if self.save(obj):
            return obj
        return None

    def create_one_a_day(
        self,
        source: dict | SQLModel,
        update: dict | None = None,
        where_dict: dict = None,
    ) -> SQLModel | None:
        """
        创建一条记录，一天仅仅就一条，会将 created_at 作为like条件，如果已经存在则不创建
        """
        if where_dict is None:
            where_dict = {}

        created_at = date_now(settings.DB_FMT)
        if "created_at" not in where_dict:
            where_dict.update({"created_at": created_at})

        where_list = [func.cast(self.model.created_at, String).like(f"%{created_at}%")]

        for key, value in where_dict.items():
            if key != "created_at":
                where_list.append(getattr(self.model, key) == value)

        count = self.get_count(and_(*where_list))
        if count > 0:
            logging.info("create_one_a_day failed, already exists.")
            return None
        else:
            return self.create(source, update)  # Create

    def create_or_update(
        self, source: dict | SQLModel, update: dict | None = None
    ) -> SQLModel | None:
        obj = self.convert_without_saving(source, update)
        if obj is None:
            return None
        pk = self.model.__mapper__.primary_key_from_instance(obj)
        if pk[0] is not None:
            existing = self.session.get(self, pk)
            if existing is None:
                return None  # Error
            else:
                existing.update(obj)  # Update
                return obj
        else:
            return self.create(obj)  # Create

    # https://github.com/tiangolo/sqlmodel/issues/494
    def get_count(self, where_statement: dict | ColumnElement) -> int:
        statement = select(self.model)

        if isinstance(where_statement, dict):
            for key, value in where_statement.items():
                statement = statement.where(getattr(self.model, key) == value)
        else:
            statement = statement.where(where_statement)

        q = statement

        count_q = (
            q.with_only_columns(func.count())
            .order_by(None)
            .select_from(q.get_final_froms()[0])
        )

        self.compile(statement)

        iterator = self.session.execute(count_q)
        for count in iterator:
            return count[0]
        return 0

    def save(self, data: SQLModel | list[SQLModel]) -> bool:
        self.session.add(data)
        try:
            self.session.commit()
            self.session.refresh(data)
            return True
        except (IntegrityError, OperationalError, FlushError) as e:
            logging.error(e)
            self.session.rollback()
            return False

    def update(self, update_dict: dict | SQLModel, where_dict: dict | SQLModel):
        try:  # 尝试获取模型
            statement = select(self.model)
            for key, value in where_dict.items():
                statement = statement.where(getattr(self.model, key) == value)
            fetched_model = self.session.exec(statement).first()
        except Exception:
            raise ValueError("Provided model doesn't exist.")  # 模型不存在，抛出错误

        if isinstance(update_dict, SQLModel):
            update_dict = update_dict.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(fetched_model, key, value)  # 更新获取到的模型，而不是传入的模型

        self.save(fetched_model)
        return fetched_model

    def delete(self, where_statement: dict | ColumnElement = None):
        if where_statement is None:
            where_statement = {}
        statement = delete(self.model)

        if isinstance(where_statement, dict):
            for key, value in where_statement.items():
                statement = statement.where(and_(getattr(self.model, key) == value))
        else:
            statement = statement.where(where_statement)

        self.compile(statement)
        self.session.exec(statement)
        self.session.commit()

    def all(self):
        return self.session.exec(select(self.model)).all()

    def to_pandas(self) -> pd.DataFrame:
        records = self.all()
        return pd.json_normalize([r.model_dump() for r in records], sep="_")

    # https://github.com/tiangolo/sqlmodel/issues/215
    def sqlmodel_to_df(
        self, statements: SelectOfScalar, set_index: bool = True
    ) -> pd.DataFrame:
        """Converts SQLModel objects into a Pandas DataFrame.
        Usage
        ----------
        df = sqlmodel_to_df(list_of_sqlmodels)
        Parameters
        ----------
        :param objects: List[SQLModel]: List of SQLModel objects to be converted.
        :param statements: ColumnElement: SQLAlchemy statement to be executed.
        :param set_index: bool: Sets the first column, usually the primary key, to dataframe index.
        """
        self.compile(statements)
        objects = self.session.exec(statements).all()

        if len(objects) > 0:
            records = [obj.model_dump() for obj in objects]
            columns = list(objects[0].model_json_schema()["properties"].keys())
            df = pd.DataFrame.from_records(records, columns=columns)
            return df.set_index(columns[0]) if set_index else df
        return pd.DataFrame()

    def df_to_sqlmodel(self, df: pd.DataFrame, refresh: bool = False):
        """Convert a pandas DataFrame into a a list of SQLModel objects."""
        # objs = [self.model(**row).model_dump() for row in df.to_dict("records")]

        self.session.bulk_insert_mappings(self.model, df.to_dict("records"))
        # for obj in objs:
        #     self.session.add(obj)
        self.session.commit()

        # if refresh:
        #     for obj in objs:
        #         self.session.refresh(obj)
        #     return objs


class SymbolActiveRecordMixin(ActiveRecordMixin):
    def __init__(
        self,
        model: type[SQLModel],
        session: Session,
    ):
        super().__init__(model, session)
        self.indicator = IndicatorsConfigMixin()

    def select_symbols(self):
        raise NotImplementedError()

    def select_max_trade_date_by_symbol(self, symbol: str):
        raise NotImplementedError()

    def get_recent_ohlc_by_symbol_and_date(
        self, symbol: str, date: str, max_days: int
    ) -> pd.DataFrame:
        raise NotImplementedError()

    @staticmethod
    def adjust(df: pd.DataFrame, last_adj_factor: float) -> pd.DataFrame:
        for prefix in ["open", "high", "low", "close"]:
            df[f"{prefix}_hfq"] = df.apply(
                lambda row, p=prefix: round(row[p] * row["adj_factor"], 4),
                axis=1,
            )
            df[f"{prefix}_qfq"] = df.apply(
                lambda row, p=prefix: round(
                    row[p] * row["adj_factor"] / last_adj_factor, 4
                ),
                axis=1,
            )
        return df

    @timer_decorator
    def add_unique_dataframe(self, df: pd.DataFrame, period: str):
        if not df.empty:
            symbol_code = df["symbol_code"].values[0]

            statement = and_(
                self.model.symbol_code == symbol_code,
            )
            order_by = col(self.model.date).desc()

            statement = select(self.model).where(statement).order_by(order_by).limit(1)
            result = self.session.exec(statement).first()

            if result:
                last_trade_date = result.date

                if period != "D":
                    self.session.delete(result)
                    self.session.commit()

                df["_date"] = pd.to_datetime(df["date"])

                if period != "D":
                    df = df.loc[df["_date"] >= last_trade_date]
                else:
                    df = df.loc[df["_date"] > last_trade_date]
                df = df.drop(columns=["_date"])

            self.df_to_sqlmodel(df)

    @staticmethod
    def get_ohlc_from_df(
        df: pd.DataFrame, col_name: [str], rename: dict = None
    ) -> pd.DataFrame:
        df_selected = df[col_name]
        if rename:
            df_selected.rename(columns=rename, inplace=True)
        return df_selected

    def technical_indicator(self, df_src: pd.DataFrame) -> pd.DataFrame:
        df = self.indicator.calculate(df_src)
        return df
