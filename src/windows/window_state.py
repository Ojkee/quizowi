from abc import ABC, abstractmethod
from typing import Optional

import raylib as rl

from src.contexts import Context


class WindowState(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_input(
        self, key: rl.KeyboardKey, mouse: Optional[tuple[int, int]] = None
    ) -> None:
        pass

    @abstractmethod
    def draw(self, ctx: Context) -> None:
        pass
