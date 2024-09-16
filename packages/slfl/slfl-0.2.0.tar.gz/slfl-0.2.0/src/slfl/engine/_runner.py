from dataclasses import dataclass
from functools import cached_property
from ._types import Task, SlotID, SlotGraph, SlotMemory
from ._traversal import find_next_slot


def _get_inputs(task: Task) -> list[SlotID]:
    return task.depends_on or []


def _get_outputs(task: Task) -> list[SlotID]:
    if isinstance(task.provides, str):
        return [task.provides]
    else:
        return task.provides


def _build_provider_graph(tasks: list[Task]) -> SlotGraph:
    graph: dict[SlotID, set[SlotID]] = {}
    for task in tasks:
        inputs = _get_inputs(task)
        outputs = _get_outputs(task)
        for input_id in inputs:
            for output_id in outputs:
                graph.setdefault(output_id, set()).add(input_id)

    return {output: list(inputs) for output, inputs in graph.items()}


class Runner:
    @dataclass
    class Stats:
        n_finished: int
        n_total: int
        job_finished: bool

    def __init__(self, tasks: list[Task], memory: SlotMemory):
        self._memory = memory
        self._tasks = tasks

    @cached_property
    def producer_index(self) -> dict[SlotID, Task]:
        return {
            output_id: task for task in self._tasks for output_id in _get_outputs(task)
        }

    @cached_property
    def slot_graph(self):
        return _build_provider_graph(self._tasks)

    def run_next(self) -> bool:
        """
        Runs next resolver function and returns False.

        If there's no more slot to resolve, returns True.
        """
        if (
            next_slot := find_next_slot(
                graph=self.slot_graph,
                memory=self._memory,
            )
        ) is not None:
            next_task = self.producer_index[next_slot]

            input_names = _get_inputs(next_task)
            fn_kwargs = {name: self._memory.get_value(name) for name in input_names}

            retval = next_task.resolver(**fn_kwargs)

            if isinstance(next_task.provides, str):
                # Single output
                output_ids = [next_task.provides]
                output_vals = [retval]
            else:
                # Multiple outputs
                output_ids = next_task.provides
                output_vals = retval

            for output_id, output_val in zip(output_ids, output_vals):
                self._memory.set_value(slot_id=output_id, value=output_val)

            return False
        else:
            return True

    @property
    def stats(self) -> Stats:
        all_slots = {*self.slot_graph.keys()} | {
            dep for deps in self.slot_graph.values() for dep in deps
        }
        slot_finished = {slot: self._memory.has_value(slot) for slot in all_slots}

        n_finished = sum(1 for finished in slot_finished.values() if finished)
        n_total = len(all_slots)
        return self.Stats(
            n_finished=n_finished,
            n_total=n_total,
            job_finished=(n_finished == n_total),
        )
