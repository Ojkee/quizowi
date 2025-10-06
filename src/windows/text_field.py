from typing import Callable, NamedTuple, Optional
from src.contexts.context import Context
import raylib as rl


class Rect(NamedTuple):
    x: int
    y: int
    w: int
    h: int

    def aslist(self) -> list[int]:
        return [self.x, self.y, self.w, self.h]


class TextField:
    PAD: int = 4
    ROUNDNESS: float = 0.6

    def __init__(self, data: str = "") -> None:
        self._inner: Optional[Rect] = None
        self._outer: Optional[Rect] = None
        self._data = data

    def set_size(self, x: int, y: int, w: int, h: int) -> None:
        self._inner = Rect(
            x + self.PAD, y + self.PAD, w - 2 * self.PAD, h - 2 * self.PAD
        )
        self._outer = Rect(x, y, w, h)

    def clicked(self, mouse: tuple[int, int]) -> bool:
        assert self._inner and self._outer
        mx, my = mouse[0], mouse[1]
        return (
            self._outer.x <= mx
            and mx <= self._outer.x + self._outer.w
            and self._outer.y <= my
            and my <= self._outer.y + self._outer.h
        )

    def draw(
        self, ctx: Context, text_drawer: Callable[[bytes, int, int], None]
    ) -> None:
        assert self._inner and self._outer
        rl.DrawRectangleRounded(
            self._outer.aslist(), self.ROUNDNESS, 0, ctx.CONSTANTS.COLORS.LIGHT_GREY
        )
        rl.DrawRectangleRounded(
            self._inner.aslist(), self.ROUNDNESS, 0, ctx.CONSTANTS.COLORS.DARK_GREY
        )
        text_drawer(self.text.encode("utf-8"), self._outer.x, self._outer.y)

    @property
    def text(self) -> str:
        return self._data

    @text.setter
    def text(self, value: str) -> None:
        self._data = value

    @property
    def width(self) -> int:
        assert self._outer
        return self._outer.w

    @property
    def height(self) -> int:
        assert self._outer
        return self._outer.h
