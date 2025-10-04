from .task import Task


class StartServer(Task):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.port: int = port


class StopServer(Task):
    pass
