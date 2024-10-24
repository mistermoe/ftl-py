def verb(func):
    func._is_ftl_verb = True
    return func
# import functools
# import inspect
# from typing import Any, Callable, Optional, TypeVar, Union, get_type_hints
#
# from ftl.constants import in_schema_extraction_mode
# from xyz.block.ftl.v1.schema import schema_pb2 as schemapb
#
# F = TypeVar("F", bound=Callable[..., Any])
#
# def verb(func: Optional[F] = None) -> Union[F, Callable[[F], F]]:
#     func._is_ftl_verb = True
#     def actual_decorator(fn: F) -> F:
#         if in_schema_extraction_mode():
#             type_hints = get_type_hints(fn)
#             sig = inspect.signature(fn)
#             first_param = next(iter(sig.parameters))
#
#             input_type = type_hints[first_param]
#             output_type = type_hints["return"]
#
#             verb = schemapb.Verb(
#                 name=fn.__name__,
#                 request=schemapb.Type(ref=schemapb.Ref(module=input_type.__module__, name=input_type.__name__)),
#                 response=schemapb.Type(ref=schemapb.Ref(module=output_type.__module__, name=output_type.__name__)),
#             )
#             # # Print the fields of input/output if they're dataclasses
#             # if hasattr(input_type, "__annotations__"):
#             #     print("\nInput fields:")
#             #     for field_name, field_type in input_type.__annotations__.items():
#             #         print(f"  - {field_name}: {field_type.__name__}")
#             #
#             # if hasattr(output_type, "__annotations__"):
#             #     print("\nOutput fields:")
#             #     for field_name, field_type in output_type.__annotations__.items():
#             #         print(f"  - {field_name}: {field_type.__name__}")
#
#         @functools.wraps(fn)
#         def wrapper(*args, **kwargs):
#             if in_schema_extraction_mode():
#                 print(f"Skipping execution of function '{func.__name__}' in static analysis mode")
#                 return None  # Do not execute the function body in static analysis mode
#             else:
#                 # Execute the actual function during normal runtime
#                 print(f"Executing")
#                 return fn(*args, **kwargs)
#
#         return wrapper
#
#     if func is not None:
#         return actual_decorator(func)
#
#     return actual_decorator