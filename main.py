import argparse
from typing import List, Optional

from app import (
    DATA_PATH, Task, add_task, clear_tasks,
    load_tasks, save_tasks, toggle_task, remove_task, get_tasks
)


def format_tasks(tasks: List[Task]) -> str:
    if not tasks:
        return "No tasks yet. Add one with: python main.py add \"Task title\""
    lines = []
    for task in tasks:
        status = "[x]" if task.done else "[ ]"
        desc = f" - {task.description}" if task.description else ""
        lines.append(f"{task.id:>2} {status} {task.title}{desc}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tiny task tracker for Git collaboration practice."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list コマンド
    list_parser = subparsers.add_parser("list", help="Show current tasks.")
    list_parser.add_argument(
        "--done", action="store_true", help="Show only completed tasks."
    )
    list_parser.add_argument(
        "--not-done", action="store_true", help="Show only not completed tasks."
    )

    # add コマンド
    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("title", help="Title for the task.")
    add_parser.add_argument(
        "--description", "-d", help="Optional description for the task."
    )

    # toggle コマンド
    toggle_parser = subparsers.add_parser("toggle", help="Mark/unmark a task by id.")
    toggle_parser.add_argument("id", type=int, help="Id of the task to flip.")

    # remove コマンド
    remove_parser = subparsers.add_parser("remove", help="Remove a task by id.")
    remove_parser.add_argument("id", type=int, help="Id of the task to remove.")

    # clear コマンド
    subparsers.add_parser("clear", help="Remove all tasks (deletes the data file).")

    args = parser.parse_args()
    tasks = load_tasks()

    if args.command == "list":
        if args.done:
            tasks_to_show = get_tasks(tasks, done=True)
        elif args.not_done:
            tasks_to_show = get_tasks(tasks, done=False)
        else:
            tasks_to_show = tasks
        print(format_tasks(tasks_to_show))

    elif args.command == "add":
        added = add_task(args.title, tasks, description=getattr(args, "description", None))
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

    elif args.command == "remove":
        try:
            removed = remove_task(args.id, tasks)
        except ValueError as exc:
            parser.error(str(exc))
        save_tasks(tasks)
        print(f"Removed task {removed.id}: {removed.title}")

    elif args.command == "clear":
        clear_tasks()
        print(f"Removed {DATA_PATH}.")


if __name__ == "__main__":
    main()
