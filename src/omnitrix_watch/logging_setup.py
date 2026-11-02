"""Logging configuration for the Omnitrix Watch project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from omnitrix_watch.config import LoggingConfig


class PrivacyFilter(logging.Filter):
    """Filter to ensure sensitive data patterns are not logged."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Check for potential token or key leaks in message
        msg = str(record.msg)
        if any(term in msg.lower() for term in ["authkey", "pairing_token", "secret_key"]):
            record.msg = "[REDACTED SECURITY DATA]"
        return True


def setup_logging(config: Optional[LoggingConfig] = None) -> logging.Logger:
    """Initialize application logging with privacy guards."""
    if config is None:
        config = LoggingConfig()

    level = getattr(logging, config.level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid duplicate handlers if called multiple times
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(PrivacyFilter())
    root_logger.addHandler(console_handler)

    if config.log_to_file:
        try:
            log_path = Path(config.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.addFilter(PrivacyFilter())
            root_logger.addHandler(file_handler)
        except Exception as e:
            root_logger.warning("Failed to configure file logger at %s: %s", config.log_file, e)

    logger = logging.getLogger("omnitrix_watch")
    logger.info("Omnitrix Watch logging initialized at level %s", config.level)
    return logger
