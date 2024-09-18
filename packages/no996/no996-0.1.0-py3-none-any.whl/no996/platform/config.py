import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AmqpDsn,
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Notify(BaseSettings):
    BARK_URL: str = None


class NetProxy(BaseSettings):
    """
    网络代理配置
    """

    # 是否启用代理
    PROXY_ENABLE: bool = False

    # 代理类型
    PROXY_TYPE: str | None = None
    # 代理服务器
    PROXY_SERVER: str | None = None
    # 代理端口
    PROXY_PORT: int | None = None
    # 代理用户名
    PROXY_USER: str | None = None
    # 代理密码
    PROXY_PASSWORD: str | None = None

    @property
    def PROXY_URI(self):
        url = f"{self.PROXY_SERVER}:{self.PROXY_PORT}"
        if self.PROXY_USER and self.PROXY_PASSWORD:
            url = f"{self.PROXY_USER}:{self.PROXY_PASSWORD}@{url}"

        if self.PROXY_TYPE:
            url = f"{self.PROXY_TYPE}://{url}"
        return url.lower()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str,
        BeforeValidator(parse_cors),
    ] = []

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    AMQP_SERVER: str
    AMQP_PORT: int = 5432
    AMQP_USER: str
    AMQP_PASSWORD: str

    @computed_field
    @property
    def AMQP_URI(self) -> AmqpDsn:
        return MultiHostUrl.build(
            scheme="amqp",
            username=self.AMQP_USER,
            password=self.AMQP_PASSWORD,
            host=self.AMQP_SERVER,
            port=self.AMQP_PORT,
        )

    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str

    @computed_field
    @property
    def REDIS_URI(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme="redis",
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
        )

    @computed_field
    @property
    def TASKIQ_BACKEND_URI(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme="redis",
            host=self.REDIS_SERVER,
            username="default",
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
            path="0",
        )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    # Tushare 配置
    TUSHARE_SCORE: int = 5000
    TUSHARE_TOKEN: str = ""

    TUSHARE_FMT: str = "YYYYMMDD"
    TUSHARE_MONTH_FMT: str = "YYYYMM"
    TUSHARE_SLEEP_TIME: float = 0.05

    ASTOCK_START_DATE: str = "20000101"
    HK_START_DATE: str = "20000101"
    TUSHARE_MAX_DEFAULT_DATE: str = "21990101"
    DB_MAX_DEFAULT_DATE: str = "2199-01-01"
    # 计算指标最小日期
    TECH_MINI_START_DATE: str = "2010-01-01"

    TIME_ZONE: str = "Asia/Shanghai"
    # database date format
    DB_FMT: str = "YYYY-MM-DD"
    DB_FMT2: str = "%Y-%m-%d"
    DB_TIME_FMT: str = "YYYY-MM-DD HH:mm:ss"

    # 配置代理信息
    proxy: NetProxy = NetProxy()

    notify: Notify = Notify()

    # 账户初始日期
    ACCOUNT_INITIAL_DATE: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()
