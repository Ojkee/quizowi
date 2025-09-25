class Colors:
    DARK_GREY: list[int] = [51, 51, 51, 255]
    BEIGE: list[int] = [255, 238, 201, 255]


class Constants:
    COLORS: Colors = Colors()


class Settings:
    BACKGROUND_COLOR: list[int] = Colors.DARK_GREY


class Context:
    CONSTANTS: Constants = Constants()
    SETTINGS: Settings = Settings()
