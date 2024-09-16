import importlib
import inspect
import logging
import re
import sys
from datetime import datetime, timezone
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType

from .engine import Task, SlotID, JobID, Runner, YamlMemory


LOG = logging.getLogger(__name__)


def task(
    *,
    description: str | None = None,
    depends_on: list[SlotID] | None = None,
    provides: SlotID | list[SlotID] | None = None,
):
    def _inner(fn):
        if depends_on is not None:
            input_slot_ids = depends_on
        else:
            param_names = list(inspect.signature(fn).parameters.keys())
            # Looks like we rely on the parameter order in 'inspect.signature()'
            # but it shouldn't matter because later on we only pass values via
            # '**kwargs', never '*args'.
            input_slot_ids = param_names or None

        if provides is not None:
            output_slot_ids = provides
        else:
            output_slot_ids = fn.__name__

        fn.task = Task(
            name=fn.__name__,
            resolver=fn,
            description=description,
            depends_on=input_slot_ids,
            provides=output_slot_ids,
        )
        return fn

    return _inner


def find_tasks_in_module(mod: ModuleType) -> list[Task]:
    fns = inspect.getmembers(mod, inspect.isfunction)
    tasks = []
    for _, fn in fns:
        try:
            task = fn.task  # type: ignore
        except AttributeError:
            continue

        tasks.append(task)

    return tasks


@contextmanager
def _prepend_to_path(sys_path: list[str], addition: str):
    orig_path = list(sys_path)
    sys_path.insert(0, addition)
    try:
        yield
    finally:
        sys_path[:] = orig_path


def load_module_file(file_path: Path) -> ModuleType:
    with _prepend_to_path(sys.path, addition=str(file_path.parent)):
        module = importlib.import_module(file_path.stem, None)

    return module


def resolve_job_id(
    tasks_file: Path, memory_dir: Path, memory_file: Path | None
) -> JobID:
    if memory_file is not None:
        job_id = memory_file.stem
        LOG.info("Resuming job %s", job_id)
        return job_id
    else:
        job_id = gen_job_id(tasks_file, memory_dir=memory_dir)
        LOG.info("Starting a new job %s", job_id)
        return job_id


def exec_all(tasks_file: Path, memory_file: Path | None):
    module = load_module_file(tasks_file)
    tasks = find_tasks_in_module(module)

    memory_dir = get_memory_dir()

    job_id = resolve_job_id(
        tasks_file=tasks_file, memory_dir=memory_dir, memory_file=memory_file
    )
    memory = YamlMemory.for_job(dir_path=memory_dir, job_id=job_id)

    runner = Runner(tasks=tasks, memory=memory)
    stats = runner.stats
    if stats.job_finished:
        LOG.info("No more tasks to run! Job %s is finished.", job_id)
    else:
        LOG.info("Task %s/%s", stats.n_finished + 1, stats.n_total)

    runner.run_next()


def get_memory_dir() -> Path:
    return Path("memory")


def gen_job_id(tasks_file: Path, memory_dir: Path) -> JobID:
    instant = _now_local()
    sep = "-"
    date_str = instant.date().isoformat()
    job_name = f"{date_str}{sep}{tasks_file.stem}"

    try:
        job_numbers = [
            int(match.group(1) or 1)
            for path in memory_dir.iterdir()
            if (match := re.match(re.escape(job_name) + r"(\d+)?", path.name))
            is not None
        ]
    except FileNotFoundError:
        job_numbers = []

    if len(job_numbers) == 0:
        return job_name
    else:
        next_number = max(job_numbers) + 1
        return f"{job_name}{next_number}"


def _now_local() -> datetime:
    return datetime.now(timezone.utc).astimezone()
