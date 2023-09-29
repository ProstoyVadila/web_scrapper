import os
import sys

import uvicorn


def main():
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
