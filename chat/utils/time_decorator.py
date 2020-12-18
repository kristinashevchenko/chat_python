import time
from collections.abc import Callable
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("time_decorator")


def time_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        time_end = time.time()
        exec_time = time_end - time_start
        logger.info(f'Execution time of {func.__name__} : {exec_time}')

    return wrapper
