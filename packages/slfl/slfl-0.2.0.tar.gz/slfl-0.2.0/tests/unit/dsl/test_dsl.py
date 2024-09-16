import logging
import shutil
import sys
from pathlib import Path

from freezegun import freeze_time
from pytest import LogCaptureFixture, MonkeyPatch, fixture
from slfl._dsl import (
    find_tasks_in_module,
    get_memory_dir,
    gen_job_id,
    load_module_file,
    resolve_job_id,
)

from ...example_proj.sample import tasks as sample_tasks


class TestLoadModuleFile:
    @staticmethod
    def test_sample_file(tmp_path: Path):
        # Given
        starting_sys_path = list(sys.path)
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()

        tasks_file = tasks_dir / "tasks_file.py"
        shutil.copy(sample_tasks.__file__, tasks_file)

        # When
        module = load_module_file(tasks_file)

        # Then
        assert module is not None
        assert "amount_transfered_to_main" in dir(module)
        assert sys.path == starting_sys_path, "Shouldn't alter global sys.path"


class TestResolveJobID:
    @staticmethod
    def test_id_not_passed(caplog: LogCaptureFixture):
        # Given
        tasks_file = Path("tasks/sample.py")
        memory_dir = Path("memory")
        memory_file = None

        with caplog.at_level(logging.INFO):
            # When
            resolved = resolve_job_id(
                tasks_file=tasks_file,
                memory_dir=memory_dir,
                memory_file=memory_file,
            )

        # Then
        assert resolved is not None
        assert tasks_file.stem in resolved
        assert "Starting" in caplog.text

    @staticmethod
    def test_id_passed(caplog: LogCaptureFixture):
        # Given
        tasks_file = Path("tasks/sample.py")
        memory_dir = Path("memory")
        memory_file = Path("memory/foo-123.yaml")

        with caplog.at_level(logging.INFO):
            # When
            resolved = resolve_job_id(
                tasks_file=tasks_file,
                memory_dir=memory_dir,
                memory_file=memory_file,
            )

        # Then
        assert resolved == "foo-123"
        assert "Resuming job foo-123" in caplog.text


class TestFindTasksInModule:
    @staticmethod
    def test_sample_tasks():
        tasks = find_tasks_in_module(sample_tasks)
        assert len(tasks) == 3
        assert tasks[0].name == "amount_transfered_to_main"
        assert tasks[1].name == "side_account_balance"
        assert tasks[2].name == "transfer_to_savings"


class TestGetMemoryDir:
    @staticmethod
    def test_standard(tmp_path: Path, monkeypatch: MonkeyPatch):
        monkeypatch.chdir(tmp_path)

        memory_dir = get_memory_dir()

        assert memory_dir.name == "memory"
        assert memory_dir.absolute().parent == tmp_path.absolute()


class TestGenJobID:
    @fixture
    @staticmethod
    def mem_dir(tmp_path: Path) -> Path:
        return tmp_path / "memory"

    class TestRelativeTasksPath:
        @fixture
        @staticmethod
        def tasks_file():
            return Path("tasks/sample.py")

        @staticmethod
        @freeze_time("2024-08-24")
        def test_empty_mem(tasks_file: Path, mem_dir: Path):
            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == "2024-08-24-sample"

        @staticmethod
        @freeze_time("2024-08-24")
        def test_existing_jobs(tasks_file: Path, mem_dir: Path):
            mem_dir.mkdir(exist_ok=True)
            (mem_dir / "2024-08-24-sample.yaml").touch()
            (mem_dir / "2024-08-24-sample2.yaml").touch()

            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == "2024-08-24-sample3"

        @staticmethod
        @freeze_time("2024-08-24")
        def test_multiple_digits(tasks_file: Path, mem_dir: Path):
            mem_dir.mkdir(exist_ok=True)
            n_prev_ids = 13
            for _ in range(n_prev_ids):
                prev_job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)
                (mem_dir / f"{prev_job_id}.yaml").touch()

            job_id = gen_job_id(tasks_file=tasks_file, memory_dir=mem_dir)

            assert job_id == f"2024-08-24-sample{n_prev_ids + 1}"
