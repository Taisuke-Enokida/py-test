import argparse
from typing import List

from app import DATA_PATH, Task, add_task, clear_tasks, load_tasks, save_tasks, toggle_task


def format_tasks(tasks: List[Task]) -> str:
    if not tasks:
        return "No tasks yet. Add one with: python main.py add \"Task title\""
    lines = []
    for task in tasks:
        status = "[x]" if task.done else "[ ]"
        lines.append(f"{task.id:>2} {status} {task.title}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny task tracker for Git collaboration practice.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Show current tasks.")

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("title", help="Title for the task.")

    toggle_parser = subparsers.add_parser("toggle", help="Mark/unmark a task by id.")
    toggle_parser.add_argument("id", type=int, help="Id of the task to flip.")

    subparsers.add_parser("clear", help="Remove all tasks (deletes the data file).")

    args = parser.parse_args()
    tasks = load_tasks()

    if args.command == "list":
        print(format_tasks(tasks))
    elif args.command == "add":
        added = add_task(args.title, tasks)
        save_tasks(tasks)
        print(f"Added: {added.id} {added.title}")
    elif args.command == "toggle":
        try:
            toggled = toggle_task(args.id, tasks)
        except ValueError as exc:
            parser.error(str(exc))
        save_tasks(tasks)
        state = "done" if toggled.done else "not done"
        print(f"Task {toggled.id} is now {state}.")
    elif args.command == "clear":
        clear_tasks()
        print(f"Removed {DATA_PATH}.")


if __name__ == "__main__":
    main()
