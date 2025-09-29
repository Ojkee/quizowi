from abc import ABC


class Event(ABC):
    pass


class StartServer(Event):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.port: int = port


class StopServer(Event):
    pass
