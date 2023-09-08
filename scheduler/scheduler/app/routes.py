from aiohttp import web

from .handlers import get_ping, start_consume

# set aiohttp routes
routes = [
    # web.get('/'),
    web.get('/ping', get_ping),
    web.post('/consume/start', start_consume),
]