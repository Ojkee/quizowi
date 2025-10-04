from dataclasses import dataclass

from typing import TYPE_CHECKING

from .task import Task

if TYPE_CHECKING:
    from src.windows.window_state import WindowState


@dataclass(frozen=True)
class StartServer(Task):
    port: int


@dataclass(frozen=True)
class StopServer(Task):
    pass


@dataclass(frozen=True)
class ChangeWindowState(Task):
    window_state: "WindowState"
