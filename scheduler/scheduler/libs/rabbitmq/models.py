from enum import Enum

from pydantic import BaseModel
from pika.exchange_type import ExchangeType


class RabbitExchange(BaseModel):
    name: str
    durable: bool = True
    auto_delete: bool = False
    exchange_type: ExchangeType = ExchangeType.direct
    arguments: dict = {}


class RabbitQueue(BaseModel):
    name: str
    exchange: RabbitExchange = None
    durable: bool = True
    exclusive: bool = False
    auto_delete: bool = False
    routing_key: str = ''
    arguments: dict = {}
