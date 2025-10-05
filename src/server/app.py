import threading
from typing import Optional
from queue import Queue

from src.observers import EventBus
from src.tasks import Task, QuitApp, StartServer, StopServer
from src.server.core import ServerSocket
from src.windows import Window, ServerMenu, ServerLobby
from src.contexts import Context


class ServerApp:
    def __init__(self) -> None:
        self.running = threading.Event()
        self.running.set()

        self._event_bus = EventBus()
        self._window = Window(ServerMenu(self._event_bus))
        self._socket: Optional[ServerSocket] = None

        self.ctx = Context()
        self.ctx.load_font("dijkstra.ttf")

        self._sniffer_t = threading.Thread(target=self._event_sniffer)
        self.tasks: Queue[Task] = Queue()

    def run(self) -> None:
        self._sniffer_t.start()
        self._window.loop(self.ctx, self.tasks)

        self.tasks.put(QuitApp())

    def _event_sniffer(self) -> None:
        while self.running.is_set():
            match self.tasks.get(block=True):
                case QuitApp():
                    self._quit()
                case StartServer(port=port) if not self._socket:
                    self._open_lobby(port)
                case StopServer() if self._socket:
                    self._close_lobby()
                case task:
                    print(f"throw away: {task.__class__.__name__}")

    def _quit(self) -> None:
        self.running.clear()
        self._clear()

    def _open_lobby(self, port: int) -> None:
        self._socket = ServerSocket(self._event_bus, port)
        self._socket.start()
        self._window.change_state(ServerLobby(self._event_bus))

    def _close_lobby(self) -> None:
        assert self._socket, "Can use that method only if socket is initialized"
        self._socket.stop()
        self._socket = None
        self._window.change_state(ServerMenu(self._event_bus))

    def _clear(self) -> None:
        self._sniffer_t.join()
        if self._socket:
            self._socket.stop()
            self._socket = None
