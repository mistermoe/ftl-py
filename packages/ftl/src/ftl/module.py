import functools
import inspect
from typing import Any, Callable, Dict, Optional, TypeVar, Union, get_type_hints

F = TypeVar("F", bound=Callable[..., Any])


class Module:
    def __init__(self):
        self._verb_registry: Dict[str, dict] = {}

    def verb(self, func: Optional[F] = None) -> Union[F, Callable[[F], F]]:  # noqa: F821
        def actual_decorator(fn: F) -> F:
            type_hints = get_type_hints(fn)
            sig = inspect.signature(fn)
            first_param = next(iter(sig.parameters))

            self._verb_registry[fn.__name__] = {
                "func": fn,
                "input_type": type_hints[first_param],
                "output_type": type_hints["return"],
            }

            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)

            return wrapper

        if func is not None:
            return actual_decorator(func)

        return actual_decorator

    def get_verbs(self):
        return self._verb_registry
