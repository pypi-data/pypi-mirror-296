from slfl.engine._traversal import find_next_slot, iter_topo_sort
from slfl.engine._types import SlotGraph
from .memory_fakes import DictMemory

from pytest import fixture


class TestIterTopoSort:
    @staticmethod
    def test_three_nodes():
        graph = {"c": ["a", "b"]}
        sequence = list(iter_topo_sort(graph=graph))
        assert sequence == ["a", "b", "c"]

    @staticmethod
    def test_disjoint():
        graph = {"c": ["a", "b"], "f": ["d", "e"]}
        sequence = list(iter_topo_sort(graph=graph))
        assert sequence == ["a", "b", "d", "e", "c", "f"]


class TestFindNextSlot:
    class TestDisjointGraph:
        @fixture
        @staticmethod
        def graph():
            return {"c": ["a", "b"], "f": ["d", "e"]}

        @staticmethod
        def test_empty_memory(graph: SlotGraph):
            memory = DictMemory({})

            slot = find_next_slot(graph=graph, memory=memory)

            assert slot == "a"

        @staticmethod
        def test_some_memory(graph: SlotGraph):
            memory = DictMemory({"a": "A", "b": "B"})

            slot = find_next_slot(graph=graph, memory=memory)

            assert slot == "d"

        @staticmethod
        def test_full_memory(graph: SlotGraph):
            memory = DictMemory(
                {
                    "a": "foo",
                    "b": "foo",
                    "c": "foo",
                    "d": "foo",
                    "e": "foo",
                    "f": "foo",
                }
            )

            slot = find_next_slot(graph=graph, memory=memory)

            assert slot is None

    class TestThreeNodes:
        @fixture
        @staticmethod
        def graph():
            return {"b": ["c"], "a": ["b"]}

        @staticmethod
        def test_1st_step(graph: SlotGraph):
            memory = DictMemory({})

            slot = find_next_slot(graph=graph, memory=memory)

            assert slot == "c"

        @staticmethod
        def test_2nd_step(graph: SlotGraph):
            memory = DictMemory({"c": "C"})

            slot = find_next_slot(graph=graph, memory=memory)

            assert slot == "b"
