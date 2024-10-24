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
            verb = schemapb.Verb(
                pos=schemapb.Position(filename=self.file_path, line=node.lineno, column=node.col_offset),
                name=func.__name__,
                request=request_type,
                response=response_type,
                export=getattr(func, "_is_ftl_export", False)
            )
            self.context.add_verb(self.module_name, verb)
        except Exception as e:
            print(f"Error extracting Verb: {e}")

        print()