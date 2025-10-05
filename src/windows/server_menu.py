from functools import cache
from typing import Optional

import raylib as rl
from src.observers import EventBus
from src.tasks import Task, StartServer
from src.windows import WindowState
from src.contexts import Context


class ServerMenu(WindowState):
    MIN_PORT: int = 1024
    MAX_PORT: int = 49151
    MAX_PORT_ENTER: int = 99999
    DEFAULT_PORT: int = 8080

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.enter_text = b"enter port:"
        self._port_number: int = self.DEFAULT_PORT

    def handle_input(self) -> Optional[Task]:
        match rl.GetKeyPressed():
            case number if rl.KEY_ZERO <= number and number <= rl.KEY_NINE:
                self._append_to_port(number)
            case rl.KEY_BACKSPACE:
                self._port_number //= 10
            case rl.KEY_ENTER:
                port = (
                    self._port_number if self._is_port_in_range() else self.DEFAULT_PORT
                )
                return StartServer(port)

        return None

    def draw(self, ctx: Context, width: int, height: int) -> None:
        text_drawer = self._center_text_drawer(ctx, width, height)
        text_drawer(self.enter_text, -32)
        # TODO: make rectangle background for port number
        text_drawer(self._port_to_bytes(self._port_number), 0)
        if not self._is_port_in_range():
            range_text: str = (
                f"Not in range [{self.MIN_PORT}, {self.MAX_PORT}], will set '{self.DEFAULT_PORT}'"
            )
            text_drawer(range_text.encode(), 64)

    def _append_to_port(self, rl_key_number: int) -> None:
        new_port = 10 * self._port_number + rl_key_number - rl.KEY_ZERO
        self._port_number = min(new_port, self.MAX_PORT_ENTER)

    @cache
    def _port_to_bytes(self, number: int) -> bytes:
        return str(number).encode()

    def _is_port_in_range(self) -> bool:
        return self.MIN_PORT <= self._port_number and self._port_number <= self.MAX_PORT
