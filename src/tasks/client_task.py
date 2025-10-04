from .task import Task


class ConnectToServer(Task):
    def __init__(self, ip: str, port: int) -> None:
        super().__init__()
        self.ip: str = ip
        self.port: int = port


class DisconnectFromServer(Task):
    pass
