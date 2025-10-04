from typing import Optional


from src.windows.window_state import WindowState
from src.tasks.task import Task
from src.contexts.context import Context


class Placeholder(WindowState):
    def __init__(self) -> None:
        super().__init__()

    def draw(self, ctx: Context, width: int, height: int) -> None:
        text_drawer = self._center_text_drawer(ctx, width, height)
        text_drawer(b"PLACEHOLDER", 0)

    def handle_input(self) -> Optional[Task]:
        return None
