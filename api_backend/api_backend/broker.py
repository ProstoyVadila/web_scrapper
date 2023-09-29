import asyncio

from loguru import logger
from aiormq import AMQPConnectionError
from propan import RabbitBroker

from api_backend.config import get_config

AMQP_CONNECTION_ERROR_INTERVAL = 5  # seconds
URLS_TO_CRAWL_EXCHANGE = "urls_to_crawl_exchange"
URLS_TO_CRAWL_QUEUE = "urls_to_crawl"

conf = get_config()
rabbit_broker = RabbitBroker(
    host=conf.rabbitmq.host,
    port=conf.rabbitmq.port,
    user=conf.rabbitmq.user,
    password=conf.rabbitmq.password,
    vhost=conf.rabbitmq.vhost,
)


async def init_broker():
    while True:
        try:
            await rabbit_broker.connect()
            break
        except AMQPConnectionError:
            logger.error("RabbitMQ is not ready, retrying in 5 seconds")
            await asyncio.sleep(AMQP_CONNECTION_ERROR_INTERVAL)
        # TODO: fix this
        except KeyboardInterrupt:
            logger.info("Stopping api backend")
            break
