from dataclasses import dataclass

from .task import Task


@dataclass(frozen=True)
class StartServer(Task):
    port: int


@dataclass(frozen=True)
class StopServer(Task):
    pass


@dataclass(frozen=True)
class EnterGamePicker(Task):
    pass


@dataclass(frozen=True)
class StartGame(Task):
    game_name: str


@dataclass(frozen=True)
class StopGame(Task):
    pass
