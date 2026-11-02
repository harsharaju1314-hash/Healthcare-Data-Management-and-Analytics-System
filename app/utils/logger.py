"""
Logging Configuration
Provides structured and leveled logging across all application modules.
"""

import logging
import sys
from pathlib import Path
from config import get_config

config = get_config()


def setup_logger(name: str = "healthcare_app") -> logging.Logger:
    """Configures and returns a named logger instance."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
        logger.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler if log file path configured
        try:
            log_file = Path(config.LOG_FILE)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass  # Fall back to console only if file logging is not writable

    return logger


logger = setup_logger()
