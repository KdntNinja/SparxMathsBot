import logging
from functools import wraps
from typing import Callable, Any

from .logger_setup import setup_logger

logger = setup_logger()


def log_function_call(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to log function entry and exit with error handling."""

    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Entering function: {func.__name__}")
        try:
            result = func(self, *args, **kwargs)
            logger.debug(f"Exiting function: {func.__name__}")
            return result
        except Exception as e:
            logger.exception(f"Error in function '{func.__name__}': {e}")
            raise

    return wrapper
