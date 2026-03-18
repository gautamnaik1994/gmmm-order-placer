import logging
import os
import sys
from typing import Final

_DEFAULT_LEVEL: Final[str] = "INFO"


def configure_logging(*, level: str | None = None) -> None:
    """Configure app-wide logging.

    Logs to stdout so that process managers (PM2/systemd/docker) can capture it.
    Includes timestamp, logger name, and source file/line.

    Idempotent: safe to call multiple times.
    """

    root = logging.getLogger()
    if getattr(root, "_gmmm_logging_configured", False):
        return

    chosen_level = (level or os.getenv("LOG_LEVEL") or _DEFAULT_LEVEL).upper()

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z",
    )
    handler.setFormatter(formatter)

    # Make configuration deterministic even if other libs configured logging earlier.
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(chosen_level)

    logging.captureWarnings(True)

    # Marker so we don't add duplicate handlers on re-import/restart.
    setattr(root, "_gmmm_logging_configured", True)
