import time
from collections.abc import Callable


def time_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        time_end = time.time()
        exec_time = time_end - time_start
        print(f'Execution time of {func.__name__} : {exec_time}')

    return wrapper
