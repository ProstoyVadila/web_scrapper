# import os
# import sys

import uvicorn
from api_backend.logger import log


# # TODO: fix logger and set logger to uvicorn
# def init_logger():
#     log_level = os.environ.get("LOG_LEVEL")
#     log_level = log_level if log_level else "INFO"
#     kek = logger.add(
#         sys.stderr,
#         format="{time} {level} {message}",
#         filter="my_module",
#         level=log_level,
#         backtrace=True,
#         diagnose=True,
#         serialize=True,
#     )


def main():
    # init_logger()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        # reload=True,
        log_level="info",
        workers=8,
    )
