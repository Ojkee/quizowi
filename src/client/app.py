import threading
from typing import Optional
from queue import Queue

from src.tasks import Task, QuitApp, ConnectToServer
from src.client.core import ClientSocket
from src.windows import Window, ClientMenu
from src.contexts import Context


class ClientApp:
    def __init__(self) -> None:
        self.running = threading.Event()
        self.running.set()

        self._window = Window(ClientMenu())
        self._socket: Optional[ClientSocket] = None

        self.ctx = Context()
        self.ctx.load_font("dijkstra.ttf")

        self._sniffer_t = threading.Thread(target=self._event_sniffer)
        self.tasks: Queue[Task] = Queue()

    def run(self) -> None:
        self._sniffer_t.start()
        self._window.loop(self.ctx, self.tasks)

        self.tasks.put(QuitApp())
        self._clear()

    def _event_sniffer(self) -> None:
        while self.running.is_set():
            match self.tasks.get(block=True):
                case QuitApp():
                    self.running.clear()
                case ConnectToServer(ip=ip, port=port):
                    print(ip, port)
                case task:
                    print(f"throw away: {task.__class__.__name__}")

    def _clear(self) -> None:
        self._sniffer_t.join()
        if self._socket:
            self._socket.stop()
            self._socket = None
