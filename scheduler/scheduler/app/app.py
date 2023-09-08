from aiohttp import web
from loguru import logger

from config import Config

from .routes import routes

def init_app(config: Config) -> web.Application:
    logger.info('Initializing app')
    app = web.Application()

    app.add_routes(routes)
    app['config'] = config

    return app

