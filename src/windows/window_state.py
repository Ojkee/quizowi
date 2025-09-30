from abc import ABC, abstractmethod
from typing import Optional

from src.tasks import Task
from src.contexts import Context


class WindowState(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_input(self) -> Optional[Task]:
        pass

    @abstractmethod
    def draw(self, ctx: Context, width: int, height: int) -> None:
        pass
