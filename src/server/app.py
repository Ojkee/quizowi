import threading
from typing import Optional
from src.tasks import Task, StartServer, QuitApp
from src.server.core import ServerSocket
from src.windows import Window, ServerMenu
from src.contexts import Context
from queue import Queue


class ServerApp:
    def __init__(self) -> None:
        self.running: threading.Event = threading.Event()
        self.running.set()

        self._window: Window = Window(ServerMenu())
        self._socket: Optional[ServerSocket] = None

        self.ctx: Context = Context()
        self.ctx.load_font("dijkstra.ttf")

        self.threads: list[threading.Thread] = [
            threading.Thread(target=self._event_sniffer),
            threading.Thread(target=self._socket_handler),
        ]
        self.tasks: Queue[Task] = Queue()

    def run(self) -> None:
        for t in self.threads:
            t.start()
        self._window.loop(self.ctx, self.tasks)

        for t in self.threads:
            t.join()

    def _event_sniffer(self) -> None:
        while self.running.is_set():
            match self.tasks.get(block=True):
                case QuitApp():
                    self.running.clear()
                case StartServer(port=_):
                    pass

    def _socket_handler(self) -> None:
        while self.running.is_set():
            if self._socket:
                self._socket.run()
