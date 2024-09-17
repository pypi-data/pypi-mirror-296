import functools
import time
from .utils import pretty_print


def timeview(func):
    @functools.wraps(func)
    def wrapper(request, /, *args, **kwargs):
        t1 = time.perf_counter_ns()
        result = func(request, *args, **kwargs)
        t2 = time.perf_counter_ns()
        pretty_print(f"Function time ({func.__name__})", f"{(t2 - t1) / 1_000_000}ms")
        return result

    return wrapper
