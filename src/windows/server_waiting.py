from typing import Optional

import raylib as rl
from src.contexts.context import Context
from src.windows import WindowState
from src.tasks.task import Task


class ServerWaiting(WindowState):
    def __init__(self) -> None:
        super().__init__()
        self._player_list: list[str] = []

    def handle_input(self) -> Optional[Task]:
        return super().handle_input()

    def draw(self, ctx: Context, width: int, height: int) -> None:
        for i, player in enumerate(self._player_list):
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

        return super().draw(ctx, width, height)

    def update_player_list(self, player_list: list[str]) -> None:
        self._player_list = player_list
