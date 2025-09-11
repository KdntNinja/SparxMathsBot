"""Logging setup for SparxMathsBot."""

import logging


def setup_logger(
    name: str = "SparxTTWorkflow", log_file: str = "workflow_log.txt"
) -> logging.Logger:
    """Set up and configure logger with both console and file handlers."""
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file, mode="w")

    console_handler.setFormatter(log_formatter)
    file_handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_function_call(func):
    """Decorator to log function entry and exit."""
    from functools import wraps

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger = logging.getLogger("SparxTTWorkflow")
        logger.debug(f"Entering function: {func.__name__}")
        try:
            result = func(self, *args, **kwargs)
            logger.debug(f"Exiting function: {func.__name__}")
            return result
        except Exception as e:
            logger.exception(f"Error in function '{func.__name__}': {e}")
            raise

    return wrapper
