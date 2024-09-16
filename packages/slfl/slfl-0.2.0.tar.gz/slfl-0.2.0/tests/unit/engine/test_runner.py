from unittest.mock import Mock

from pytest import fixture
from .memory_fakes import DictMemory
from slfl.engine._types import Task
from slfl.engine._runner import Runner


class TestRunner:
    @staticmethod
    @fixture
    def two_tasks():
        return [
            Task(
                name="task1",
                resolver=Mock(return_value="A"),
                provides="a",
                depends_on=None,
            ),
            Task(
                name="task2",
                resolver=Mock(return_value="B"),
                provides="b",
                depends_on=["a"],
            ),
        ]

    @staticmethod
    @fixture
    def memory():
        return DictMemory({})

    class TestRunNext:
        @staticmethod
        def test_sample_interaction(two_tasks, memory):
            runner = Runner(two_tasks, memory)

            runner.run_next()
            two_tasks[0].resolver.assert_called_with()

            runner.run_next()
            two_tasks[1].resolver.assert_called_with(a="A")

    class TestStats:
        @staticmethod
        def test_sample_interaction(two_tasks, memory):
            runner = Runner(two_tasks, memory)
            assert runner.stats.n_finished == 0
            assert runner.stats.n_total == 2
            assert runner.stats.job_finished is False

            _ = runner.run_next()
            assert runner.stats.n_finished == 1
            assert runner.stats.n_total == 2
            assert runner.stats.job_finished is False

            _ = runner.run_next()
            assert runner.stats.n_finished == 2
            assert runner.stats.n_total == 2
            assert runner.stats.job_finished is True
