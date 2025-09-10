import logging
import logging.handlers
import os
from pathlib import Path

LOG_FILE = Path("logs/book_api.log").absolute()

def configure_logger():
    """Configure logging: Console + Rotating File"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger()   # root logger
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
