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
    /* 全体のスタイル */
    body {{
      font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
      max-width: 720px;
      margin: 40px auto;
      padding: 0 16px;
      /* グラデーション背景を追加 */
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      color: #1b1b1f;
    }}
    
    /* タイトルとサブタイトル */
    h1 {{
      margin-bottom: 6px;
      color: #ffffff;
      font-size: 2.2em;
      font-weight: 700;
      text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    p.sub {{
      margin-top: 0;
      /* コメント通り、ここは黒にする（数行だけ黒く） */
      color: #000000;
      font-size: 0.95em;
    }}
    
    /* メインカード */
    .card {{
      background: #ffffff;
      padding: 28px;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      /* ホバー時に少し浮き上がる効果 */
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 24px 70px rgba(0,0,0,0.35);
    }}
    
    /* フォームのスタイル */
    form.add {{
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
    }}
    form.add input[type=text] {{
      flex: 1;
      padding: 12px 16px;
      border-radius: 12px;
      border: 2px solid #e2e8f0;
      font-size: 15px;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}
    /* 入力フィールドにフォーカスした時のスタイル */
    form.add input[type=text]:focus {{
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* ボタンの基本スタイル */
    button {{
      cursor: pointer;
      border: none;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 12px 20px;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }}
    button:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }}
    button:active {{
      transform: translateY(0);
      box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }}
    button.secondary {{
      background: #f1f5f9;
      color: #475569;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    button.secondary:hover {{
      background: #e2e8f0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    /* タスクリスト */
    ul {{
      list-style: none;
      padding: 0;
      margin: 16px 0;
      display: grid;
      gap: 10px;
    }}
    li {{
      background: #f8fafc;
      border: 2px solid #e2e8f0;
      border-radius: 12px;
      padding: 14px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.3s ease;
    }}
    /* タスクアイテムにホバーした時の効果 */
    li:hover {{
      background: #f1f5f9;
      border-color: #cbd5e1;
      transform: translateX(4px);
    }}
    /* 完了したタスクのスタイル */
    li[data-status="done"] {{
      background: #f0fdf4;
      border-color: #bbf7d0;
    }}
    li[data-status="done"] .title {{
      text-decoration: line-through;
      color: #6b7280;
    }}
    
    /* トグルボタン */
    button.toggle {{
      width: 40px;
      height: 40px;
      padding: 0;
      font-size: 18px;
      background: #ffffff;
      color: #111;
      border: 2px solid #e2e8f0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border-radius: 10px;
      transition: all 0.2s ease;
    }}
    button.toggle:hover {{
      border-color: #667eea;
      transform: scale(1.1);
    }}
    
    li .title {{
      flex: 1;
      font-size: 15px;
      font-weight: 500;
      /* タスクのタイトルは常に黒にする（未完了は黒、完了は既存のグレー） */
      color: #000000;
    }}
    
    /* 通知メッセージ */
    .notice {{
      background: linear-gradient(135deg, #ecfeff 0%, #cffafe 100%);
      border: 2px solid #67e8f9;
      padding: 12px 16px;
      border-radius: 10px;
      color: #0f172a;
      margin-bottom: 16px;
      font-weight: 500;
      /* フェードインアニメーション */
      animation: fadeIn 0.3s ease;
    }}
    @keyframes fadeIn {{
      from {{
        opacity: 0;
        transform: translateY(-10px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    
    .empty {{
      color: #94a3b8;
      font-style: italic;
      text-align: center;
      padding: 20px;
    }}
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
