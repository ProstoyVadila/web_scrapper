from loguru import logger
from pydantic_settings import BaseSettings
from pydantic import Field


class RabbitMQConfig(BaseSettings):
    host: str = Field('localhost', env='RABBITMQ_HOST')
    port: int = Field(5672, env='RABBITMQ_PORT')
    username: str = Field('guest', env='RABBITMQ_ADMIN_USER')
    password: str = Field('guest', env='RABBITMQ_ADMIN_PASSWORD')
    vhost: str = Field('/', env='RABBITMQ_VHOST')
    queue_names: list[str] = Field(..., env='RABBITMQ_QUEUE_NAMES')
    exchange_names: list[str] = Field(..., env='RABBITMQ_EXCHANGE_NAMES')


    @property
    def amqp_url(self):
        return f'amqp://{self.username}:{self.password}@{self.host}'


class Config(BaseSettings):
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    log_level: str = Field('INFO', env='LOG_LEVEL')


def get_config():
    logger.info('Loading config')
    return Config()
