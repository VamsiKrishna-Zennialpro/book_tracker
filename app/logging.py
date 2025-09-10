import logging
import logging.handlers
import os
from pathlib import Path

LOG_FILE = Path("logs/book_api.log").absolute()
#LOG_FILE = C:\Github\fullstack-agentic-ai\articles\fastapi\code-samples\BOOK-TRACKER-API\app\logs\book-api.log

def configure_logger():
    """Configure the logging for the application : Console and File Logging (Rotational)"""

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #Configure console handler for logging  
    console_handler =  logging.StreamHandler() # Print on Screen
    console_handler.setLevel(logging.INFO) # Set the Level
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # Log Rotation Handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes= 104857760, # 10 MB log file
        backupCount= 5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)    
    file_format = logging.Formatter(
         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter (file_format)

    # Attach the File and Console handler with Logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

logger = logging.getLogger(__name__)