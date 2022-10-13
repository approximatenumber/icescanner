import logging
import time
from functools import wraps

logger = logging.getLogger("wrappers")


def retry(retries=3, time_between_retries=0, exception_class=Exception):
    if callable(retries):
        original_decorated_function = retries
        retries = 3
    else:
        original_decorated_function = None

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            current_try = retries
            logger.debug(f"Will execute '{func.__name__}' for {retries} times")
            while True:
                try:
                    return func(*args, **kwargs)
                except exception_class as e:
                    if current_try > 0:
                        logger.error(f"Exception {type(e)}: {e} occurred. Retrying for {current_try - 1}")
                        current_try -= 1
                        time.sleep(time_between_retries)
                    else:
                        logger.error("Retry limit exhausted, raising")
                        raise

        return wrapped

    if original_decorated_function is not None:
        return wrapper(original_decorated_function)
    else:
        return wrapper


def profiler(func):
    """ Measure execution time of given function and log it"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        delta = time.time() - time_start
        logger.debug(f"{func} execution took {delta} secs")
        return res

    return wrapper


def log_exception(func):
    """ Catch exceptions in given function and log it instead of raising"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.critical(f"Execute function '{func.__name__}' ignoring exception if occurred")
            return func(*args, **kwargs)
        except Exception as e:
            logger.critical(f"Exception '{e}' occurred when '{func.__name__}' called with args/kwargs: {args, kwargs}")

    return wrapper
