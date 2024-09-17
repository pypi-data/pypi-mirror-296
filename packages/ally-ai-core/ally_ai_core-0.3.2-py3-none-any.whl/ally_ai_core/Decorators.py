from contextlib import contextmanager
import logging
import inspect
from functools import wraps
from typing import Optional


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




from time import perf_counter
from typing import Optional, Callable, TypeVar, Any

F = TypeVar('F', bound=Callable[..., Any])

def timed(_func: Optional[F] = None, *, message: Optional[str] = None, level: int = logging.INFO) -> Callable[..., F]:
    """
    A decorator that logs the time taken by a function to execute.
    Can be used with or without arguments.

    Usage:
        @timed
        def func(...):
            ...

        @timed(message="Custom message", level=logging.DEBUG)
        def func(...):
            ...
    """
    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start = perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    elapsed = perf_counter() - start
                    log_message = f"{func.__name__} took {elapsed:.6f} seconds to finish"
                    if message:
                        log_message = f"{message} - {log_message}"
                    logging.log(level, f"Timed: {log_message}")
            return async_wrapper  # type: ignore
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start = perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed = perf_counter() - start
                    log_message = f"{func.__name__} took {elapsed:.6f} seconds to finish"
                    if message:
                        log_message = f"{message} - {log_message}"
                    logging.log(level, f"Timed: {log_message}")
            return sync_wrapper  # type: ignore

    if _func is None:
        # Decorator is called with arguments
        return decorator
    else:
        # Decorator is used without arguments
        return decorator(_func)
