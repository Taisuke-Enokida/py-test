from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

DATA_PATH = Path(__file__).parent / "data" / "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False


def load_tasks(path: Path = DATA_PATH) -> List[Task]:
    if not path.exists():
        return []
    try:
        raw = path.read_text(encoding="utf-8") or "[]"
        data = json.loads(raw)
        return [Task(**item) for item in data]
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error loading tasks: {e}")
        return []


def save_tasks(tasks: List[Task], path: Path = DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(task) for task in tasks]
    try:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"Error saving tasks: {e}")


def add_task(title: str, tasks: List[Task], description: Optional[str] = None) -> Task:
    new_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=new_id, title=title.strip(), description=description)
    tasks.append(task)
    return task


def toggle_task(task_id: int, tasks: List[Task]) -> Task:
    for task in tasks:
        if task.id == task_id:
            task.done = not task.done
            return task
    raise ValueError(f"Task with id {task_id} not found.")


def remove_task(task_id: int, tasks: List[Task]) -> Task:
    for i, task in enumerate(tasks):
        if task.id == task_id:
            removed = tasks.pop(i)
            return removed
    raise ValueError(f"Task with id {task_id} not found.")


def clear_tasks(path: Path = DATA_PATH) -> None:
    if path.exists():
        path.unlink()


def get_tasks(tasks: List[Task], done: Optional[bool] = None) -> List[Task]:
    """done=Trueなら完了タスクのみ、done=Falseなら未完了のみ、Noneなら全て"""
    if done is None:
        return tasks
    return [task for task in tasks if task.done == done]
