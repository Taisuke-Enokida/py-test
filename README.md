## Simple Python Task Tracker

Lightweight CLI app for practicing Git collaboration. It stores tasks in a local JSON file and uses only the Python standard library.

### Setup
- Requires Python 3.10+ (uses `dataclasses` and `pathlib` only).
- No external dependencies or virtual environment needed.

### CLI Usage
Run commands from the repo root (use `python3` if `python` is not available):

```bash
# List tasks
python3 main.py list

# Add a new task
python3 main.py add "Write the README"

# Mark/unmark a task by id
python3 main.py toggle 1

# Clear all tasks
python3 main.py clear
```

### Browser (optional)
簡易Web UIを標準ライブラリだけで用意しました。

```bash
python3 server.py
# -> open http://localhost:8000 in your browser
```

タスクの追加/完了切り替え/全消去がブラウザから行えます。

Tasks are stored in `data/tasks.json`. The file is created automatically if it does not exist.
