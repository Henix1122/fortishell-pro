import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(
    name="fortishell",
    log_file=None,
    level=logging.INFO,
    max_bytes=5 * 1024 * 1024,
    backup_count=3,
    fmt='[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    propagate=False
):
    """
    Setup and return a robust logger with console and optional rotating file output.

    Args:
        name (str): Logger name.
        log_file (str): Path to log file (optional).
        level (int): Logging level.
        max_bytes (int): Max size per log file before rotation.
        backup_count (int): Number of backup files to keep.
        fmt (str): Log message format.
        datefmt (str): Date format.
        propagate (bool): Whether to propagate logs to parent.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate

    formatter = logging.Formatter(fmt, datefmt=datefmt)

    # Console handler (stream to stderr for errors, stdout otherwise)
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Rotating file handler
    if log_file and not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Usage example:
# from utils.logger import setup_logger
# log = setup_logger(log_file="app.log", level=logging.DEBUG)
# log.info("SSL check started on example.com")
# log.error("Certificate validation failed")
