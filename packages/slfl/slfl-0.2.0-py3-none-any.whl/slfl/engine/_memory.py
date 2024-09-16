from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from ruamel.yaml import YAML

from ._types import JobID, SlotID


class YamlMemory:
    def __init__(self, file_path: Path):
        self._file_path = file_path

    @classmethod
    def for_job(cls, dir_path: Path, job_id: JobID):
        dir_path.mkdir(parents=True, exist_ok=True)
        return cls(file_path=dir_path / f"{job_id}.yaml")

    @property
    @contextmanager
    def slot_dict(self) -> Generator[dict[str, Any], None, None]:
        yaml = YAML()
        try:
            yaml_dict = yaml.load(self._file_path)
        except FileNotFoundError:
            yaml_dict = self._make_empty_dict()

        yield yaml_dict.setdefault("slots", {})

        yaml.dump(yaml_dict, self._file_path)

    @staticmethod
    def _make_empty_dict():
        return {}

    def get_value(self, slot_id: SlotID) -> Any | None:
        with self.slot_dict as slots:
            return slots.get(slot_id)

    def has_value(self, slot_id: SlotID) -> bool:
        with self.slot_dict as slots:
            return slot_id in slots

    def set_value(self, slot_id: SlotID, value: Any):
        with self.slot_dict as slots:
            slots[slot_id] = value
