from contextlib import contextmanager
import logging
import sys
import inspect
from functools import wraps


@contextmanager
def log_step(name: str, level=logging.INFO, raise_exception: bool = True):
    try:
        logging.log(level=level, msg=f"Step({name}): Executing...")
        yield
        logging.log(level=level, msg=f"Step({name}): Executed.")
    except Exception as ex:
        logging.error(f"Step({name}): Failed! Reason: {ex}")

        if raise_exception:
            raise

def logstep(message: str, level=logging.INFO, show_start: bool = True, show_finish: bool = True):
    """
    Decorator to log the start and finish of function execution.

    Args:
        message (str): Custom message to include in logs.
        level (int): Logging level.
        show_start (bool): Whether to log the start of the function.
        show_finish (bool): Whether to log the finish of the function.
    """
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def awrapper(*args, **kwargs_wrapper):
                if show_start:
                    logging.log(level, f"{message} - Starting {func.__name__} with args: {args}, kwargs: {kwargs_wrapper}")
                
                result = await func(*args, **kwargs_wrapper)
                
                if show_finish:
                    logging.log(level, f"{message} - Finished {func.__name__} with result: {result}")
                return result
            return awrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs_wrapper):
                if show_start:
                    logging.log(level, f"{message} - Starting {func.__name__} with args: {args}, kwargs: {kwargs_wrapper}")
                
                result = func(*args, **kwargs_wrapper)
                
                if show_finish:
                    logging.log(level, f"{message} - Finished {func.__name__} with result: {result}")
                return result
            return wrapper
    return decorator



from time import time

def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        elapsed = time() - start
        logging.info(f"{f.__name__} took {elapsed:.6f} seconds to finish")
        return result
    return wrapper