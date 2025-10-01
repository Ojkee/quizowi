import asyncio
import threading
from typing import Optional
from src.tasks import Task, QuitApp, StartServer, StopServer
from src.server.core import ServerSocket
from src.windows import Window, ServerMenu
from src.contexts import Context
from queue import Queue


class ServerApp:
    def __init__(self) -> None:
        self.running = threading.Event()
        self.running.set()

        self._window = Window(ServerMenu())
        self._socket: Optional[ServerSocket] = None

        self.ctx = Context()
        self.ctx.load_font("dijkstra.ttf")

        self._sniffer_t = threading.Thread(target=self._event_sniffer)
        self.tasks: Queue[Task] = Queue()

    def run(self) -> None:
        self._sniffer_t.start()
        self._window.loop(self.ctx, self.tasks)

        self.tasks.put(QuitApp())
        self._sniffer_t.join()
        if self._socket:
            self._socket.stop()
            self._socket.join()
            self._socket = None

    def _event_sniffer(self) -> None:
        while self.running.is_set():
            match self.tasks.get(block=True):
                case QuitApp():
                    self.running.clear()
                case StartServer(port=p) if not self._socket:
                    self._socket = ServerSocket(p)
                    self._socket.start()
                case StopServer() if self._socket:
                    self._socket.stop()
                    self._socket.join()
                    self._socket = None
                case task:
                    print(f"throw away: {task.__class__.__name__}")
