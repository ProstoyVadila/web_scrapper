import functools

import pika
import orjson
from loguru import logger
from pika.exchange_type import ExchangeType

from config import RabbitMQConfig

from .models import (
    RabbitExchange,
    RabbitQueue,
)

class RabbitMQ:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.__connection = None
        self.__channel = None
        self.__queues = set()
        self.__exchanges = set()
        self.__routing_keys = set()
        self.__handlers = {}
        self.__con_params = None

    def init(self):
        self.__con_params = pika.ConnectionParameters(
            host=self.config.host,
            port=self.config.port,
            virtual_host=self.config.virtual_host,
            credentials=pika.PlainCredentials(
                username=self.config.username,
                password=self.config.password,
            )
        )

    @property
    def connection(self) -> pika.BlockingConnection:
        if not self.__connection or self.__connection.is_closed:
            self.__connection = pika.BlockingConnection(self.__con_params)
        return self.__connection

    @property
    def channel(self) -> pika.BlockingChannel:
        if not self.__channel or self.__channel.is_closed:
            self.__channel = self.connection.channel()
        return self.__channel

    def _is_already_set(self, item: RabbitQueue | RabbitExchange) -> bool:
        match item:
            case isinstance(item, RabbitQueue):
                return item.name in self.__queues or item.routing_key in self.__routing_keys
            case isinstance(item, RabbitExchange):
                return item.name in self.__exchanges and item.exchange_type == ExchangeType.direct
            case _:
                logger.error(f'Unknown object type {type(item)} for {item}')
                return True

    def _add_exchange(self, exchange: RabbitExchange):
        if self._is_already_set(exchange):
            logger.error(f'Exchange {exchange.name} is already set')
            return

        logger.info(f'Creating exchange {exchange.name}')
        self.channel.exchange_declare(
            exchange=exchange.name,
            durable=exchange.durable,
            auto_delete=exchange.auto_delete,
            exchange_type=exchange.exchange_type.value,
            arguments=exchange.arguments,
        )
        self.__queues.add(exchange.name)

    def _add_queue(self, queue: RabbitQueue):
        if self._is_already_set(queue):
            logger.error(f'Queue {queue.name} is already set')
            return

        logger.info(f'Creating queue {queue.name}')
        self.channel.queue_declare(
            queue=queue.name,
            durable=queue.durable,
            exclusive=queue.exclusive,
            auto_delete=queue.auto_delete,
            arguments=queue.arguments,
        )
        self.channel.queue_bind(
            queue=queue.name,
            exchange=queue.exchange.name,
            routing_key=queue.routing_key,
        )
        self.__queues.add(queue.name)
        self.__routing_keys.add(queue.routing_key)

    def _set_queue(self, queue: RabbitQueue):
        self._add_exchange(queue.exchange)
        self._add_queue(queue)

    def json_wrapper(func, *args, **kwargs):
        @functools.wraps(func)
        def decorator(ch, method, properties, body):
            try:
                data = orjson.loads(body)
                res = func(data)
            except Exception as e:
                logger.error(f'Error while processing message: {e}')
                return
            if not res:
                logger.error(f'Error while processing message: {res}')
                return

            ch.basic_ack(delivery_tag=method.delivery_tag)
            return res

        return decorator

    def add_handler(self, queue: RabbitQueue, handler: callable):
        self.__handlers[queue.name] = self.json_wrapper(handler)


    def consume(self, queues: list[RabbitQueue]):
        self.channel.basic_qos(prefetch_count=1)

        for queue, handler in self.__handlers.items():
            queue = RabbitQueue(name=queue)
            self.__add_queue(queue)
            self.channel.basic_consume(
                queue=queue,
                on_message_callback=handler,
                auto_ack=False,
            )
        # for queue in queues:
        #     self.set_queue(queue)

        # for queue in queues:
        #     self.channel.basic_consume(
        #         queue=queue.name,
        #         on_message_callback=callback,
        #         auto_ack=True,
        #     )
        pass
        