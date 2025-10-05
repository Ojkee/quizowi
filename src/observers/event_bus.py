import threading
from typing import Callable, Type
from .observer import EventType

Action = Callable[[EventType], None]


class EventBus:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: dict[Type[EventType], list[Action]] = {}

    def subscribe(self, event: Type[EventType], action: Action) -> None:
        with self._lock:
            self._subscribers.setdefault(event, []).append(action)

    def publish(self, event: EventType) -> None:
        with self._lock:
            actions = list(self._subscribers.get(type(event), []))
        for action in actions:
            action(event)
