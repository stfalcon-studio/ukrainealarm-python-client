import logging
import os
import pathlib
from logging import handlers

from app.config import Config


def get_logger(cfg: Config) -> logging.Logger:
    if not pathlib.Path("log").is_dir():
        os.makedirs("log")

    logger = logging.getLogger("AlertLogger")
    logger.setLevel(cfg.log_level)
    handler = logging.handlers.RotatingFileHandler(
        pathlib.Path("log", cfg.log),
        maxBytes=cfg.log_size_bytes,
        backupCount=cfg.log_backup_count,
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(handler)
    return logger
