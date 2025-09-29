from typing import Any, Optional
import raylib as rl


class Colors:
    DARK_GREY: list[int] = [51, 51, 51, 255]
    BEIGE: list[int] = [255, 238, 201, 255]


class Constants:
    COLORS: Colors = Colors()
    FONT_SIZE_SMALL = 32


class Settings:
    BACKGROUND_COLOR: list[int] = Colors.DARK_GREY
    FONT: Optional[Any] = None


class Context:
    CONSTANTS: Constants = Constants()
    SETTINGS: Settings = Settings()

    def load_font(self, path: bytes) -> None:
        self.SETTINGS.FONT = rl.LoadFont(path)

    @property
    def font(self):
        assert self.SETTINGS.FONT, "Font need to be initialized via `load_font(path)`"
        return self.SETTINGS.FONT
