"""Entry point for running the SignalForge server.

Usage: uv run python -m signalforge
"""

import uvicorn

from signalforge.api.app import create_app
from signalforge.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    app = create_app()
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
