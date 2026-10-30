#!/usr/bin/env python3
"""open-loops scan: condense this project's past Claude Code sessions so open loops can be found in them.

Reads ~/.claude/projects/<encoded project path>/*.jsonl and prints, oldest first, each exchange as:
the user's message + Claude's final answer to it (tool calls and tool output are dropped). Claude then reads this
and adds whatever is still open to the project's open-loops list (see SKILL.md, "Scanning past sessions").

  open_loops_scan.py                 # sessions changed since the last scan (first run: last 14 days)
  open_loops_scan.py --days 30       # sessions changed in the last 30 days, ignoring the last-scan mark
  open_loops_scan.py --all           # every session of this project
  open_loops_scan.py --out FILE      # write to FILE instead of stdout (use for large output)
  open_loops_scan.py --no-mark       # do not move the last-scan mark

The current session (newest file, or $CLAUDE_SESSION_ID) is skipped. Per-answer text is cut to --max-answer chars
(default 1500) and per-message to --max-user (default 600) so the result stays readable.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

STATE_DIR = os.path.expanduser("~/.claude/open-loops")
NOISE = re.compile(r"<(system-reminder|local-command-[a-z]+|command-[a-z]+|task-notification)>.*?</\1>", re.S)


def project_root():
    try:
        return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        return os.getcwd()


def sessions_dir(root):
    return os.path.expanduser("~/.claude/projects/" + re.sub(r"[^A-Za-z0-9]", "-", root))


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for block in content or []:
        if isinstance(block, dict) and block.get("type") == "text":
            out.append(block.get("text") or "")
    return "\n".join(out)


def is_tool_result(content):
    return isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def clean(s, limit):
    s = NOISE.sub("", s or "").strip()
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s if len(s) <= limit else s[:limit] + " …[cut]"


def exchanges(path, max_user, max_answer):
    """[(timestamp, user text, final answer text)] of one session file."""
    out, user, answer, ts = [], None, "", None
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        msg = d.get("message") or {}
        if d.get("type") == "user" and msg.get("role") == "user" and not d.get("isMeta"):
            content = msg.get("content")
            if is_tool_result(content):
                continue
            t = clean(text_of(content), max_user)
            if not t:
                continue
            if user is not None:
                out.append((ts, user, answer))
            user, answer, ts = t, "", d.get("timestamp")
        elif d.get("type") == "assistant" and msg.get("role") == "assistant" and user is not None:
            t = text_of(msg.get("content"))
            if t.strip():
                answer = t  # keep the last text block: the answer the user actually read
    if user is not None:
        out.append((ts, user, clean(answer, max_answer)))
    return [(a, b, clean(c, max_answer)) for a, b, c in out]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--days", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--no-mark", action="store_true")
    ap.add_argument("--max-user", type=int, default=600)
    ap.add_argument("--max-answer", type=int, default=1500)
    a = ap.parse_args()

    root = project_root()
    sdir = sessions_dir(root)
    if not os.path.isdir(sdir):
        print(f"no sessions for {root} ({sdir})"); return 0
    os.makedirs(STATE_DIR, exist_ok=True)
    mark_file = os.path.join(STATE_DIR, os.path.basename(root) + ".scan.json")
    mark = {}
    if os.path.exists(mark_file):
        mark = json.load(open(mark_file))
    now = time.time()
    if a.all:
        since = 0
    elif a.days:
        since = now - a.days * 86400
    else:
        since = mark.get("last_scan") or now - 14 * 86400

    files = sorted((os.path.join(sdir, f) for f in os.listdir(sdir) if f.endswith(".jsonl")), key=os.path.getmtime)
    current = os.environ.get("CLAUDE_SESSION_ID")
    if current:
        files = [f for f in files if not f.endswith(current + ".jsonl")]
    elif files:
        files = files[:-1]  # newest file = this session
    files = [f for f in files if os.path.getmtime(f) >= since]

    lines = [f"# open-loops scan · {root} · {len(files)} session(s) changed since "
             f"{dt.datetime.fromtimestamp(since):%Y-%m-%d %H:%M}" if since else f"# open-loops scan · {root} · all sessions"]
    for f in files:
        ex = exchanges(f, a.max_user, a.max_answer)
        if not ex:
            continue
        lines.append(f"\n## session {os.path.basename(f)[:8]} · {ex[0][0] or '?'} → {ex[-1][0] or '?'} · {len(ex)} exchanges")
        for ts, user, answer in ex:
            lines.append(f"\n[{(ts or '')[:16]}] USER: {user}")
            if answer:
                lines.append(f"CLAUDE: {answer}")
    text = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"{a.out}: {len(files)} session(s), {len(text):,} chars")
    else:
        sys.stdout.write(text)
    if not a.no_mark:
        json.dump({"last_scan": now}, open(mark_file, "w"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
