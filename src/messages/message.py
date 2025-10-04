from abc import ABC
import dataclasses
import json


@dataclasses.dataclass
class Message(ABC):
    def as_bytes(self) -> bytes:
        self_dict = dataclasses.asdict(self)
        return json.dumps(self_dict).encode("utf-8")
