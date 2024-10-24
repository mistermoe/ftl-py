from dataclasses import dataclass

from ftl.decorators import verb, export


@dataclass
class EchoRequest:
    name: str


@dataclass
class EchoResponse:
    message: str


@verb
@export
def echo(req: EchoRequest) -> EchoResponse:
    return EchoResponse(message=f"ayooo, {req.name}!")
.