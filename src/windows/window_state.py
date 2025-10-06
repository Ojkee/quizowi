from abc import ABC, abstractmethod
from functools import cache
from typing import Callable, Optional

import raylib as rl

from src.observers import EventBus
from src.tasks import Task
from src.contexts import Context


class WindowState(ABC):
    def __init__(self, event_bus: EventBus) -> None:
        self._width: Optional[int] = None
        self._height: Optional[int] = None
        self._event_bus = event_bus

    def set_size(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    @abstractmethod
    def handle_input(self) -> Optional[Task]:
        pass

    @abstractmethod
    def draw(self, ctx: Context) -> None:
        pass

    @cache
    def _text_size(self, ctx: Context, text: bytes):
        return rl.MeasureTextEx(ctx.font, text, ctx.CONSTANTS.FONT_SIZE_SMALL, 0)

    def _center_text_drawer(
        self, ctx: Context, width: int, height: int
    ) -> Callable[[bytes, int, int], None]:
        def drawer(text: bytes, x: int, y: int) -> None:
            size = self._text_size(ctx, text)
            position = [(width - size.x) // 2 + x, (height - size.y) // 2 + y]
            rl.DrawTextEx(
                ctx.font,
                text,
                position,
                ctx.CONSTANTS.FONT_SIZE_SMALL,
                ctx.CONSTANTS.FONT_SPACING,
                ctx.CONSTANTS.COLORS.BEIGE,
            )

        return drawer
