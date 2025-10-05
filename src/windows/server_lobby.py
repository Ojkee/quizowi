from typing import Optional

import raylib as rl
from src.observers import EventBus, ClientConnected, ClientDisconnected
from src.contexts.context import Context
from src.windows import WindowState
from src.tasks.task import Task


class ServerLobby(WindowState):
    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self._players_info: list[str] = []
        self._games_info: list[str] = []

        self._event_bus.subscribe(ClientConnected, self._on_connect)
        self._event_bus.subscribe(ClientDisconnected, self._on_disconnect)

    def handle_input(self) -> Optional[Task]:
        return super().handle_input()

    def draw(self, ctx: Context, width: int, height: int) -> None:
        for i, player in enumerate(self._players_info):
            nick = player.encode("utf-8")
            size = rl.MeasureTextEx(
                ctx.font,
                nick,
                ctx.CONSTANTS.FONT_SIZE_SMALL,
                ctx.CONSTANTS.FONT_SPACING,
            )
            rl.DrawTextEx(
                ctx.font,
                nick,
                [width - size.x, i * size.y],
                ctx.CONSTANTS.FONT_SIZE_SMALL,
                ctx.CONSTANTS.FONT_SPACING,
                ctx.CONSTANTS.COLORS.BEIGE,
            )

        # draw scrollable vertically game list

        return super().draw(ctx, width, height)

    def _on_connect(self, client: ClientConnected) -> None:
        self._players_info.append(client.nick)

    def _on_disconnect(self, client: ClientDisconnected) -> None:
        self._players_info = [
            player for player in self._players_info if not player == client.nick
        ]
