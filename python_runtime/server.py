import importlib
import json
from concurrent import futures
from dataclasses import asdict

import grpc
from grpc_reflection.v1alpha import reflection

# Assuming you have your proto-generated modules
from .generated import runtime_pb2, runtime_pb2_grpc


class RuntimeService(runtime_pb2_grpc.RuntimeServicer):
    def __init__(self, module):
        self.verbs = module.get_verbs()

    def Execute(self, request, context):
        try:
            verb_info = self.verbs.get(request.verb)
            if not verb_info:
                return runtime_pb2.RuntimeResponse(
                    error=f"Unknown verb: {request.verb}"
                )

            # Parse input
            input_data = json.loads(request.payload)
            input_obj = verb_info["input_type"](**input_data)

            # Call function
            result = verb_info["func"](input_obj)

            # Serialize output
            output_data = json.dumps(asdict(result))

            return runtime_pb2.RuntimeResponse(payload=output_data.encode("utf-8"))

        except Exception as e:
            return runtime_pb2.RuntimeResponse(error=str(e))


def import_module(module_path: str):
    """
    Import a module by path and return its 'module' attribute.

    Example:
    import_module('modules.echo.echo')
    """
    try:
        imported = importlib.import_module(module_path)
        if not hasattr(imported, "module"):
            raise AttributeError(f"Module {module_path} has no 'module' attribute")
        return imported.module
    except Exception as e:
        raise ImportError(f"Failed to import {module_path}: {str(e)}")


def serve(module_path: str, port: int = 50051):
    """
    Import module and start gRPC server.

    Example:
    serve('modules.echo.echo')
    """
    # Import the module
    module = import_module(module_path)

    # Create and start server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    runtime_pb2_grpc.add_RuntimeServicer_to_server(RuntimeService(module), server)

    addr = f"[::]:{port}"
    server.add_insecure_port(addr)
    server.start()

    # Enable reflection
    SERVICE_NAMES = (
        runtime_pb2.DESCRIPTOR.services_by_name["Runtime"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    print(f"Server started on port {port}")
    print(f"Available verbs: {list(module.get_verbs().keys())}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the FTL server")
    parser.add_argument("module_path", help="Module path (e.g., modules.echo.echo)")
    parser.add_argument("--port", type=int, default=50051, help="Port to listen on")

    args = parser.parse_args()
    serve(args.module_path, args.port)
