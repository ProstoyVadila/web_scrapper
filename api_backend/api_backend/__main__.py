import os
import sys

import uvicorn
from api_backend.config import init_logger


def main():
    init_logger()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        # reload=True,
        log_level="info",
        workers=8,
    )


if __name__ == "__main__":
    main()
