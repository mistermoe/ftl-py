from concurrent import futures

import grpc


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add secure/insecure port
    server.add_insecure_port("[::]:50051")

    # todo

    # Start the server
    server.start()
    print("Server started on port 50051")

    try:
        # Keep the server running
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
