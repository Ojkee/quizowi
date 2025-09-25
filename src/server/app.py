from typing import Optional
from src.server.core import ServerSocket
from src.windows import Window, ServerMenu
from src.contexts import Context


class ServerApp:
    def __init__(self) -> None:
        self._running: bool = True
        self.ctx: Context = Context()

        self._window: Window = Window(ServerMenu())
        self._socket: Optional[ServerSocket] = None

    def run(self) -> None:
        self._window.draw(self.ctx)
        if self._socket:
            self._socket.run()
