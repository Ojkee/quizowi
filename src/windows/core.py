import raylib as rl

from src.windows.window_state import WindowState
from src.contexts import Context


class Window:
    WIDTH: int = 1200
    HEIGHT: int = 900
    TITLE: bytes = b"Quizowi"

    def __init__(self, start_state: WindowState) -> None:
        rl.InitWindow(self.WIDTH, self.HEIGHT, self.TITLE)

        self._state: WindowState = start_state

    def loop(self, ctx: Context) -> None:
        while not rl.WindowShouldClose():
            self._handle_input()
            self._draw(ctx)

    def _handle_input(self) -> None:
        self._state.handle_input()

    def _draw(self, ctx: Context) -> None:
        rl.BeginDrawing()
        rl.ClearBackground(ctx.SETTINGS.BACKGROUND_COLOR)
        self._state.draw(ctx, self.WIDTH, self.HEIGHT)
        rl.EndDrawing()

    def __exit__(self) -> None:
        rl.CloseWindow()
