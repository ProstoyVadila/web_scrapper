from propan import RabbitBroker

from config import get_config

AMQP_CONNECTION_ERROR_INTERVAL = 5  # seconds
URLS_TO_CRAWL_EXCHANGE = "urls_to_crawl_exchange"
URLS_TO_CRAWL_QUEUE = "urls_to_crawl_queue"

conf = get_config()
rabbit_broker = RabbitBroker(
    host=conf.rabbitmq.host,
    port=conf.rabbitmq.port,
    user=conf.rabbitmq.user,
    password=conf.rabbitmq.password,
    vhost=conf.rabbitmq.vhost,
)
