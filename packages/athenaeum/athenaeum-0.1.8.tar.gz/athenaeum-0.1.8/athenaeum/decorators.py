import time
import atexit
import functools
from typing import Callable, Any
from athenaeum.logger import logger
from athenaeum.browser_automation import BrowserAutomation


def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.success(f"func：`{func.__name__}` 执行花费 `{end_time - start_time:.4f}` 秒")
        return result

    return wrapper


def add_kwargs(**kwargs: Any) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*func_args: Any, **func_kwargs: Any) -> Any:
            func_kwargs = {**kwargs, **func_kwargs}
            result = func(*func_args, **func_kwargs)
            return result

        return wrapper

    return decorator


def add_cp(*args, **kwargs) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*func_args: Any, **func_kwargs: Any) -> Any:
            cp = BrowserAutomation.get_ChromiumPage(*args, **kwargs)
            atexit.register(lambda x: x.close(), cp)
            func_kwargs = {**{"cp": cp}, **func_kwargs}
            result = func(*func_args, **func_kwargs)
            return result

        return wrapper

    return decorator
