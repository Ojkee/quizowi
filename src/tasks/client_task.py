from dataclasses import dataclass
from .task import Task


@dataclass(frozen=True)
class ConnectToServer(Task):
    ip: str
    port: int
    nick: str


@dataclass(frozen=True)
class DisconnectFromServer(Task):
    pass
