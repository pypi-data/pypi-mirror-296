from dataclasses import dataclass
from pathlib import Path
import subprocess
import shutil

from pytest import MonkeyPatch, fixture
from ..example_proj.sample import tasks as tasks_mod


def _run_cmd(cmd: list[str], input: str | None = None):
    input_bytes = input.encode() if input else None
    proc = subprocess.run(
        cmd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = proc.stdout.decode()
    err = proc.stderr.decode()
    assert (
        proc.returncode == 0
    ), f"Retcode {proc.returncode}.\nstdout:\n{out}\nstderr:\n{err}"

    return out, err


@dataclass
class ProjectFixture:
    proj_dir: Path
    relative_tasks_file: Path


class TestCLI:
    @fixture
    @staticmethod
    def tmp_proj(tmp_path: Path) -> ProjectFixture:
        # Source: 'example_proj/tasks/sample.py'
        src_tasks_file = Path(tasks_mod.__file__)
        src_proj_dir = src_tasks_file.parent.parent
        src_relative = src_tasks_file.relative_to(src_proj_dir)

        # Target: '<tmp>/example_proj/tasks/sample.py'
        dest_proj_dir = tmp_path / src_proj_dir.name

        shutil.copytree(src_proj_dir, dest_proj_dir)

        return ProjectFixture(proj_dir=dest_proj_dir, relative_tasks_file=src_relative)

    @staticmethod
    def test_exec(tmp_proj: ProjectFixture, monkeypatch: MonkeyPatch):
        monkeypatch.chdir(tmp_proj.proj_dir)

        out, _ = _run_cmd(
            ["slfl", str(tmp_proj.relative_tasks_file)], input="1234"
        )

        assert "1. Go to" in out
        assert "2. Read PLN balance" in out

        mem_dir = (tmp_proj.proj_dir / "memory")
        assert mem_dir.is_dir()

        yamls = [path for path in mem_dir.iterdir() if path.suffix == ".yaml"]
        assert len(yamls) == 1
