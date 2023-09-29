import os
import sys

from loguru import logger
from pydantic import Field, Extra, ValidationError, BaseSettings
from dotenv import find_dotenv, load_dotenv

from api_backend.logger import log


ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class PostgresConfig(BaseSettings):
    host: str = Field(..., env="POSTGRES_HOST")
    port: int = Field(..., env="POSTGRES_PORT")
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    db_name: str = Field(..., env="POSTGRES_DB")

    class Config:
        env_file = os.path.join(ROOT, ".env")
        extra = Extra.ignore

    @property
    def pg_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}"


class RabbitMQConfig(BaseSettings):
    host: str = Field(..., env="RABBITMQ_HOST")
    port: int = Field(..., env="RABBITMQ_PORT")
    user: str = Field(..., env="RABBITMQ_ADMIN_USER")
    password: str = Field(..., env="RABBITMQ_ADMIN_PASSWORD")
    vhost: str = Field(..., env="RABBITMQ_VHOST")
    # queue_names: list[str] = Field(..., alias='RABBITMQ_QUEUE_NAMES')
    # exchange_names: list[str] = Field(..., alias='RABBITMQ_EXCHANGE_NAMES')

    class Config:
        env_file = os.path.join(ROOT, ".env")
        extra = Extra.ignore

    @property
    def amqp_url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class Config(BaseSettings):
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    postgres: PostgresConfig = PostgresConfig()
    log_level: str = Field("DEBUG", env="log_level")

    class Config:
        env_file = os.path.join(ROOT, ".env")
        extra = Extra.ignore


def get_config():
    log.info("Loading config")
    try:
        # return Config()
        config = Config()
        log.debug("amqp_url: {}".format(config.rabbitmq.amqp_url))
        return config
    except ValidationError as exc:
        print(repr(exc.errors()[0]["type"]))
        raise exc
