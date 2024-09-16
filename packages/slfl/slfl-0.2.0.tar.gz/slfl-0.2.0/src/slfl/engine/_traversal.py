from graphlib import TopologicalSorter
from typing import Generator
from ._types import SlotGraph, SlotID, SlotMemory


def iter_topo_sort(graph: SlotGraph) -> Generator[SlotID, None, None]:
    sorter = TopologicalSorter(graph)
    yield from sorter.static_order()


def find_next_slot(graph: SlotGraph, memory: SlotMemory) -> SlotID | None:
    for slot in iter_topo_sort(graph=graph):
        if not memory.has_value(slot):
            return slot

    return None
