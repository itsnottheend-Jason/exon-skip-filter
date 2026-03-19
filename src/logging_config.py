import logging
import os
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig

def setup_logging():
    """Configure dual console + file logging for Docker."""
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/exon-skip-filter.log",
                "maxBytes": 100*1024*1024,  # 100MB
                "backupCount": 5,
                "formatter": "standard",
                "encoding": "utf-8"
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["file", "console"]
        }
    }
    
    dictConfig(LOGGING_CONFIG)
