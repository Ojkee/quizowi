from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Task(ABC):
    pass


@dataclass(frozen=True)
class QuitApp(Task):
    pass
