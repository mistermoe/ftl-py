import functools
import inspect
from typing import Any, Callable, Optional, TypeVar, Union, get_type_hints

F = TypeVar("F", bound=Callable[..., Any])


def verb(func: Optional[F] = None) -> Union[F, Callable[[F], F]]:
    def actual_decorator(fn: F) -> F:
        # Get the actual types
        type_hints = get_type_hints(fn)
        sig = inspect.signature(fn)
        first_param = next(iter(sig.parameters))

        input_type = type_hints[first_param]
        output_type = type_hints["return"]

        # Print info like before, but now with resolved types
        print(f"Function name: {fn.__name__}")
        print("Arguments:")
        print(f"  - {first_param}: {input_type.__name__}")
        print(f"Return type: {output_type.__name__}")

        # Print the fields of input/output if they're dataclasses
        if hasattr(input_type, "__annotations__"):
            print("\nInput fields:")
            for field_name, field_type in input_type.__annotations__.items():
                print(f"  - {field_name}: {field_type.__name__}")

        if hasattr(output_type, "__annotations__"):
            print("\nOutput fields:")
            for field_name, field_type in output_type.__annotations__.items():
                print(f"  - {field_name}: {field_type.__name__}")

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    if func is not None:
        return actual_decorator(func)

    return actual_decorator
