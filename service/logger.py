import logging
from logging.handlers import RotatingFileHandler

from rich import print as rich_print


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler with colorized output
    class RichHandler(logging.StreamHandler):
        def emit(self, record):
            try:
                msg = self.format(record)
                rich_print(msg)
                self.flush()
            except Exception:
                self.handleError(record)

    console_handler = RichHandler()
    console_handler.setLevel(level)

    # Create a file handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(level)

    # Define a formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
