import functools
from typing import Any, Callable, Optional, TypeVar, Union

F = TypeVar("F", bound=Callable[..., Any])


def verb(func: Optional[F] = None) -> Union[F, Callable[[F], F]]:
    def actual_decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    # If used without parentheses
    if func is not None:
        return actual_decorator(func)

    # If used with parentheses
    return actual_decorator
