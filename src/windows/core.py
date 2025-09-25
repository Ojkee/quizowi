import raylib as rl

from src.windows.window_state import WindowState
from src.contexts import Context


class Window:
    WIDTH: int = 1200
    HEIGHT: int = 900
    TITLE: bytes = b"Quizowi"

    def __init__(self, start_state: WindowState) -> None:
        self._state: WindowState = start_state

        self._init()

    def _init(self) -> None:
        rl.InitWindow(self.WIDTH, self.HEIGHT, self.TITLE)

    def draw(self, ctx: Context) -> None:
        while not rl.WindowShouldClose():
            rl.BeginDrawing()
            rl.ClearBackground(ctx.SETTINGS.BACKGROUND_COLOR)
            self._state.draw(ctx)
            rl.EndDrawing()

    def __exit__(self) -> None:
        rl.CloseWindow()
