from queue import Queue
import threading
import raylib as rl


from src.tasks import Task, QuitApp
from src.windows.window_state import WindowState
from src.contexts import Context


class Window:
    WIDTH: int = 1200
    HEIGHT: int = 900
    TITLE: bytes = b"Quizowi"

    def __init__(self, start_state: WindowState) -> None:
        self._lock = threading.Lock()

        rl.SetTraceLogLevel(rl.LOG_NONE)
        rl.InitWindow(self.WIDTH, self.HEIGHT, self.TITLE)
        rl.SetTargetFPS(60)
        rl.SetExitKey(rl.KEY_NULL)

        self._state: WindowState = start_state
        self._state.set_size(self.WIDTH, self.HEIGHT)

    def loop(self, ctx: Context, tasks: Queue[Task]) -> None:
        while not rl.WindowShouldClose():
            self._handle_input(tasks)
            self._draw(ctx)
        tasks.put(QuitApp())

    def change_state(self, window_state: WindowState) -> None:
        with self._lock:
            self._state = window_state
            self._state.set_size(self.WIDTH, self.HEIGHT)

    def _handle_input(self, tasks: Queue[Task]) -> None:
        task = self._state.handle_input()
        if task:
            tasks.put(task)

    def _draw(self, ctx: Context) -> None:
        rl.BeginDrawing()
        rl.ClearBackground(ctx.SETTINGS.BACKGROUND_COLOR)
        self._state.draw(ctx)
        rl.EndDrawing()

    def __exit__(self) -> None:
        rl.CloseWindow()
