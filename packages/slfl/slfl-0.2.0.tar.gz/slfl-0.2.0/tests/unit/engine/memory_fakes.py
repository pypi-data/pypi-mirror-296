from typing import Any
from slfl.engine import SlotID


class DictMemory:
    """
    Matches SlotMemory protocol.
    """

    def __init__(self, values: dict[SlotID, Any]):
        self._values = dict(values)

    def get_value(self, slot_id: SlotID):
        return self._values.get(slot_id)

    def has_value(self, slot_id: SlotID) -> bool:
        return slot_id in self._values

    def set_value(self, slot_id: SlotID, value: Any):
        self._values[slot_id] = value
