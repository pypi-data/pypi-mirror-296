from dataclasses import dataclass
from typing import Any, Protocol


type SlotID = str
type JobID = str


# {"to get this slot": ["you need", "these slots first"]}
type SlotGraph = dict[SlotID, list[SlotID]]


class Resolver(Protocol):
    def __call__(self, **kwargs) -> Any:
        pass


@dataclass
class Task:
    name: str
    resolver: Resolver
    provides: SlotID | list[SlotID]
    description: str | None = None
    depends_on: list[SlotID] | None = None


class SlotMemory(Protocol):
    def get_value(self, slot_id: SlotID): ...
    def has_value(self, slot_id: SlotID) -> bool: ...
    def set_value(self, slot_id: SlotID, value: Any): ...
