"""
Tasks are objects responsible for communication between window screens and the application itself.
They operate exclusively within the application and are never transmitted through sockets.
"""

from abc import ABC


class Task(ABC):
    pass


class QuitApp(Task):
    pass


class StartServer(Task):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.port: int = port


class StopServer(Task):
    pass
