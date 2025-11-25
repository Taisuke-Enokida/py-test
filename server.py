from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from app import add_task, clear_tasks, load_tasks, save_tasks, toggle_task


def render_html(message: str | None = None) -> str:
    tasks = load_tasks()
    rows = []
    for task in tasks:
        status = "done" if task.done else "todo"
        checkbox = "[x]" if task.done else "[ ]"
        rows.append(
            f"<li data-status='{status}'>"
            f"<form method='post' style='display:inline'>"
            f"<input type='hidden' name='action' value='toggle'>"
            f"<input type='hidden' name='id' value='{task.id}'>"
            f"<button type='submit' class='toggle'>{checkbox}</button>"
            f"</form>"
            f"<span class='title'>{task.title}</span>"
            f"</li>"
        )
    task_list = "\n".join(rows) if rows else "<li class='empty'>No tasks yet.</li>"
    notice = f"<p class='notice'>{message}</p>" if message else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Task Tracker</title>
  <style>
    body {{
      font-family: 'Helvetica Neue', Arial, sans-serif;
      max-width: 720px;
      margin: 40px auto;
      padding: 0 16px;
      background: #f7f7fb;
      color: #1b1b1f;
    }}
    h1 {{ margin-bottom: 6px; }}
    p.sub {{ margin-top: 0; color: #4a5568; }}
    .card {{
      background: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }}
    form.add {{ display: flex; gap: 8px; margin-bottom: 12px; }}
    form.add input[type=text] {{
      flex: 1;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #d1d5db;
      font-size: 15px;
    }}
    button {{
      cursor: pointer;
      border: none;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      padding: 10px 14px;
      font-size: 14px;
      transition: transform 120ms ease, box-shadow 120ms ease;
      box-shadow: 0 6px 16px rgba(37,99,235,0.25);
    }}
    button:hover {{ transform: translateY(-1px); box-shadow: 0 8px 18px rgba(37,99,235,0.3); }}
    button:active {{ transform: translateY(0); }}
    button.secondary {{
      background: #e5e7eb;
      color: #1f2937;
      box-shadow: none;
    }}
    ul {{ list-style: none; padding: 0; margin: 12px 0; display: grid; gap: 8px; }}
    li {{
      background: #f8fafc;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    li[data-status="done"] .title {{ text-decoration: line-through; color: #6b7280; }}
    button.toggle {{
      width: 36px;
      height: 36px;
      padding: 0;
      font-size: 18px;
      background: #fff;
      color: #111;
      border: 1px solid #e5e7eb;
      box-shadow: none;
    }}
    li .title {{ flex: 1; }}
    .notice {{
      background: #ecfeff;
      border: 1px solid #67e8f9;
      padding: 10px 12px;
      border-radius: 8px;
      color: #0f172a;
    }}
    .empty {{ color: #94a3b8; font-style: italic; }}
  </style>
</head>
<body>
  <h1>Task Tracker</h1>
  <p class="sub">Standard-library only. Add tasks and toggle them in your browser.</p>
  <div class="card">
    {notice}
    <form class="add" method="post">
      <input type="hidden" name="action" value="add">
      <input type="text" name="title" placeholder="New task" required>
      <button type="submit">Add</button>
    </form>
    <ul>
      {task_list}
    </ul>
    <form method="post" style="margin-top:12px;">
      <input type="hidden" name="action" value="clear">
      <button type="submit" class="secondary">Clear all</button>
    </form>
  </div>
</body>
</html>"""


class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        html = render_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)
        action = form.get("action", [""])[0]

        tasks = load_tasks()
        message = None

        try:
            if action == "add":
                title = form.get("title", [""])[0].strip()
                if not title:
                    raise ValueError("Title cannot be empty.")
                add_task(title, tasks)
                save_tasks(tasks)
                message = "Task added."
            elif action == "toggle":
                task_id = int(form.get("id", ["0"])[0])
                toggle_task(task_id, tasks)
                save_tasks(tasks)
                message = f"Toggled task {task_id}."
            elif action == "clear":
                clear_tasks()
                message = "Cleared all tasks."
            else:
                message = "Unknown action."
        except ValueError as exc:
            message = str(exc)

        html = render_html(message)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def run_server(port: int = 8000) -> None:
    server = HTTPServer(("127.0.0.1", port), TaskHandler)
    print(f"Serving on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    run_server()
