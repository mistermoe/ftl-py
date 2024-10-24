from dataclasses import dataclass

from ftl import Ftl

module = Ftl.module()


@dataclass
class EchoRequest:
    name: str


@dataclass
class EchoResponse:
    message: str


@module.verb
def echo(req: EchoRequest) -> EchoResponse:
    return EchoResponse(message=f"ayooo, {req.name}!")


@dataclass
class HeheRequest:
    popo: str


@dataclass
class HeheResponse:
    soso: str


@module.verb
def hehe(req: HeheRequest) -> HeheResponse:
    return HeheResponse(soso=f"hehe, {req.popo}!")
