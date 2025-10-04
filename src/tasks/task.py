"""
Tasks are objects responsible for communication between window screens and the application itself.
They operate exclusively within the application and are never transmitted through sockets.
"""

from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Task(ABC):
    pass


@dataclass(frozen=True)
class QuitApp(Task):
    pass
