from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class EventType(ABC):
    pass


@dataclass(frozen=True)
class ClientConnected(EventType):
    nick: str


@dataclass(frozen=True)
class ClientDisconnected(EventType):
    nick: str
