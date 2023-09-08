import asyncio

import uvloop
from aiohttp import web
from loguru import logger

from app import init_app
from config import get_config


def start_scheduler():
    logger.info('Starting scheduler')
    uvloop.install()
    loop = asyncio.get_event_loop()

    config = get_config()
    app = init_app(config=config)

    web.run_app(app=app, loop=loop)


if __name__ == '__main__':
    start_scheduler()
