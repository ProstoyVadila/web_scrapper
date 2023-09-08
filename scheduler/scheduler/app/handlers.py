from aiohttp import web
from loguru import logger

async def get_ping(request):
    return web.Response(text='pong')


async def start_consume(request):
    logger.info('Start consuming')
    return web.Response(text='ok')
