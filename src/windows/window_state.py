from abc import ABC, abstractmethod
from typing import Optional

from src.events import Event
from src.contexts import Context


class WindowState(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_input(self) -> Optional[Event]:
        pass

    @abstractmethod
    def draw(self, ctx: Context, width: int, height: int) -> None:
        pass
