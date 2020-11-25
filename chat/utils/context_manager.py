import time
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("time_context_manager")


class TimeContextManager:
    def __init__(self, name="function"):
        self.name = name

    def __enter__(self):
        self.time_start = time.time()

    def __exit__(self, *args):
        end_time = time.time()
        exec_time = end_time - self.time_start
        logger.info(f'Execution time of {self.name} : {exec_time}')
