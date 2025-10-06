from functools import cache
import re
from typing import Optional

import raylib as rl
from src.observers import EventBus
from src.tasks import Task, ConnectToServer
from src.windows import WindowState
from src.windows.text_field import TextField
from src.contexts import Context


class ClientMenu(WindowState):
    MIN_PORT: int = 1024
    MAX_PORT: int = 49151
    MAX_PORT_ENTER: int = 99999
    DEFAULT_PORT: int = 8080

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self._nick: str = ""
        self.enter_port = b"enter port:"
        self._port_number: int = self.DEFAULT_PORT

        self._ip: TextField = TextField("localhost")
        self._port: TextField = TextField(str(self.DEFAULT_PORT))

    def set_size(self, width: int, height: int) -> None:
        self._ip.set_size(width // 3, 2 * height // 5, width // 3, 60)
        self._port.set_size(width // 3, 3 * height // 5, width // 3, 60)
        return super().set_size(width, height)

    def handle_input(self) -> Optional[Task]:
        match rl.GetKeyPressed():
            case rl.KEY_ENTER:
                return ConnectToServer("localhost", 8080, self._nick)

        return super().handle_input()

    def draw(self, ctx: Context) -> None:
        self._ip.draw(
            ctx,
            self._center_text_drawer(ctx, self._ip.width, self._ip.height),
        )
        self._port.draw(
            ctx,
            self._center_text_drawer(ctx, self._port.width, self._port.height),
        )

    def _append_to_port(self, rl_key_number: int) -> None:
        new_port = 10 * self._port_number + rl_key_number - rl.KEY_ZERO
        self._port_number = min(new_port, self.MAX_PORT_ENTER)

    @cache
    def _port_to_bytes(self, number: int) -> bytes:
        return str(number).encode()

    def _is_port_in_range(self) -> bool:
        return self.MIN_PORT <= self._port_number and self._port_number <= self.MAX_PORT

    def _is_ip_valid(self) -> bool:
        if self._ip.text == "localhost":
            return True
        if (
            re.match("^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$", self._ip.text)
            == None
        ):
            return False
        return True
