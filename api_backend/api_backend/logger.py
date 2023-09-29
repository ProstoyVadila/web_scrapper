import os
import sys

from loguru import logger

logger.remove()
logger.add(
    sink=lambda x: print(x),
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    serialize=True,
)

log = logger
