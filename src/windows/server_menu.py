import raylib as rl

from typing import Optional
from src.windows.window_state import WindowState
from src.contexts import Context


class ServerMenu(WindowState):
    def __init__(self) -> None:
        pass

    def handle_input(
        self, key: rl.KeyboardKey, mouse: Optional[tuple[int, int]] = None
    ) -> None:
        return super().handle_input(key, mouse)

    def draw(self, ctx: Context) -> None:
        return super().draw(ctx)
