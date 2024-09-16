import argparse
import logging
from pathlib import Path
from ._dsl import exec_all


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tasks_file", type=Path, help="Path to .py file with tasks. Should be relative."
    )
    parser.add_argument(
        "-m",
        "--memory_file",
        type=Path,
        help="Memory file to resume a job. If not passed, a new job will be started and a new memory file will be created.",
    )
    args = parser.parse_args()

    exec_all(tasks_file=args.tasks_file, memory_file=args.memory_file)

    return 0
