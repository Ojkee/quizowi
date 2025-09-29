from typing import Optional
from src.events import Event
from src.server.core import ServerSocket
from src.windows import Window, ServerMenu
from src.contexts import Context
from collections import deque


class ServerApp:
    def __init__(self) -> None:
        self._window: Window = Window(ServerMenu())
        self._socket: Optional[ServerSocket] = None

        self.ctx: Context = Context()
        self.ctx.load_font(b"/home/ojke/programming/quizowi/assets/fonts/dijkstra.ttf")

        self.event_queue: deque[Event] = deque()

    def run(self) -> None:
        self._window.loop(self.ctx)
        if self._socket:
            self._socket.run()
