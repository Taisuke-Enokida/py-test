from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).parent / "data" / "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


def load_tasks(path: Path = DATA_PATH) -> List[Task]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8") or "[]"
    data = json.loads(raw)
    return [Task(**item) for item in data]


def save_tasks(tasks: List[Task], path: Path = DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(task) for task in tasks]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def add_task(title: str, tasks: List[Task]) -> Task:
    new_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=new_id, title=title.strip())
    tasks.append(task)
    return task


def toggle_task(task_id: int, tasks: List[Task]) -> Task:
    for task in tasks:
        if task.id == task_id:
            task.done = not task.done
            return task
    raise ValueError(f"Task with id {task_id} not found.")


def clear_tasks() -> None:
    if DATA_PATH.exists():
        DATA_PATH.unlink()
