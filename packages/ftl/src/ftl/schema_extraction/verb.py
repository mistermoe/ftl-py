import ast
import inspect
from typing import get_type_hints

from ftl.schema_extraction.common import extract_type
from ftl.schema_extraction.context import LocalExtractionContext
from xyz.block.ftl.v1.schema import schema_pb2 as schemapb


class VerbExtractor(ast.NodeVisitor):
    def __init__(self, context: LocalExtractionContext, module_name, file_path):
        self.context = context
        self.module_name = module_name
        self.file_path = file_path

    def load_function(self, func_name):
        try:
            module = self.context.load_python_module(self.module_name, self.file_path)
            func = getattr(module, func_name, None)
            if func is None:
                print(f"Function {func_name} not found in {self.module_name}")
                return None
            return func
        except ImportError as e:
            print(f"Error importing module {self.module_name}: {e}")
            return None

    def visit_FunctionDef(self, node):
        func = self.load_function(node.name)
        if func is None:
            return

        func = self.load_function(node.name)
        if func is None:
            return

        if not getattr(func, "_is_ftl_verb", False):
            print(f"Function '{node.name}' does not have the 'verb' decorator")
            return

        try:
            type_hints = get_type_hints(func)
            sig = inspect.signature(func)

            first_param = next(iter(sig.parameters))

            input_type = type_hints[first_param]
            output_type = type_hints["return"]

            request_type=extract_type(self.context, input_type)
            response_type=extract_type(self.context, output_type)
            print(f"req type:{request_type}")
            print(f"resp type:{response_type}")
            verb = schemapb.Verb(
                pos=schemapb.Position(filename=self.file_path, line=node.lineno, column=node.col_offset),
                name=func.__name__,
                request=request_type,
                response=response_type,
                export=getattr(func, "_is_ftl_export", False)
            )
            self.context.add_verb(self.module_name, verb)
            print(f"input:{input_type}")
            print(f"output:{output_type}")

            # Simulate Verb creation (as in the original verb decorator)
            print(f"Simulated Verb instance for function '{func.__name__}'")
            print(f"Verb name: {verb.name}")
            print(f"Request type: {verb.request.ref.name} (module: {verb.request.ref.module})")
            print(f"Response type: {verb.response.ref.name} (module: {verb.response.ref.module})")
        except Exception as e:
            print(f"Error extracting Verb: {e}")

        print()
#
# class MockObject:
#     """A simple mock object that can have arbitrary attributes."""
#     def __init__(self, **kwargs):
#         self.__dict__.update(kwargs)
#
#     def __repr__(self):
#         return f"MockObject({self.__dict__})"
#
# def simulate_decorator_execution(func):
#     """Simulate the decorator logic by passing mock arguments."""
#     if not getattr(func, "_is_ftl_verb", False):
#         print(f"Function '{func.__name__}' does not have the 'verb' decorator")
#         return
#
#     try:
#         sig = inspect.signature(func)
#         mock_args = []
#         mock_kwargs = {}
#
#         for param in sig.parameters.values():
#             if param.default == inspect.Parameter.empty and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY):
#                 # Create a mock object with a 'name' attribute for the positional argument
#                 mock_args.append(MockObject(name="mock_name"))
#             elif param.kind == inspect.Parameter.KEYWORD_ONLY:
#                 # Pass a mock object with attributes if needed
#                 mock_kwargs[param.name] = MockObject(name="mock_name")
#
#
#         func(*mock_args, **mock_kwargs)
#     except Exception as e:
#         print(f"Error simulating decorator for function '{func.__name__}': {e}")
