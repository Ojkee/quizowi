from functools import cache
from typing import Optional

import raylib as rl
from src.observers import EventBus
from src.tasks import Task, StartServer
from src.windows import WindowState
from src.contexts import Context
from src.windows.text_field import TextField


class ServerMenu(WindowState):
    MIN_PORT: int = 1024
    MAX_PORT: int = 49151
    MAX_PORT_ENTER: int = 99999
    DEFAULT_PORT: int = 8080

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.enter_text = b"enter port:"
        self._port: TextField = TextField(str(self.DEFAULT_PORT))

    def set_size(self, width: int, height: int) -> None:
        self._port.set_size(width // 3, height // 2 - 24, width // 3, 48)
        return super().set_size(width, height)

    def handle_input(self) -> Optional[Task]:
        match rl.GetKeyPressed():
            case number if rl.KEY_ZERO <= number and number <= rl.KEY_NINE:
                self._append_to_port(number)
            case rl.KEY_BACKSPACE:
                self._cut_from_port()
            case rl.KEY_ENTER:
                port = (
                    int(self._port.text)
                    if self._is_port_in_range()
                    else self.DEFAULT_PORT
                )
                return StartServer(port)

        return None

    def draw(self, ctx: Context) -> None:
        assert (
            self._width and self._height
        ), "Window state size must be set `.set_size(width, height)`"

        text_drawer = self._center_text_drawer(ctx, self._width, self._height)
        text_drawer(self.enter_text, 0, -32)
        self._port.draw(
            ctx, self._center_text_drawer(ctx, self._port.width, self._port.height)
        )
        if not self._is_port_in_range():
            range_text: str = (
                f"Not in range [{self.MIN_PORT}, {self.MAX_PORT}], will set '{self.DEFAULT_PORT}'"
            )
            text_drawer(range_text.encode(), 0, 64)

    def _append_to_port(self, rl_key_number: int) -> None:
        new_port = (
            10 * (int(self._port.text) if self._port.text else 0)
            + rl_key_number
            - rl.KEY_ZERO
        )
        self._port.text = self._port.text if new_port > self.MAX_PORT else str(new_port)

    def _cut_from_port(self) -> None:
        if self._port.text:
            self._port.text = str(int(self._port.text) // 10)

    @cache
    def _port_to_bytes(self, number: int) -> bytes:
        return str(number).encode()

    def _is_port_in_range(self) -> bool:
        return (
            not self._port.text == ""
            and self.MIN_PORT <= int(self._port.text)
            and int(self._port.text) <= self.MAX_PORT
        )
