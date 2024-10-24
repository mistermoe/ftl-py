# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from . import runtime_pb2 as runtime__pb2

GRPC_GENERATED_VERSION = "1.67.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + " but the generated code in runtime_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class RuntimeStub(object):
    """Define the Runtime service"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Execute = channel.unary_unary(
            "/Runtime/Execute",
            request_serializer=runtime__pb2.RuntimeRequest.SerializeToString,
            response_deserializer=runtime__pb2.RuntimeResponse.FromString,
            _registered_method=True,
        )


class RuntimeServicer(object):
    """Define the Runtime service"""

    def Execute(self, request, context):
        """Execute a verb in a module"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_RuntimeServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Execute": grpc.unary_unary_rpc_method_handler(
            servicer.Execute,
            request_deserializer=runtime__pb2.RuntimeRequest.FromString,
            response_serializer=runtime__pb2.RuntimeResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "Runtime", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("Runtime", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class Runtime(object):
    """Define the Runtime service"""

    @staticmethod
    def Execute(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/Runtime/Execute",
            runtime__pb2.RuntimeRequest.SerializeToString,
            runtime__pb2.RuntimeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
