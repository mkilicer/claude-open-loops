#!/bin/bash
# SessionStart hook for the open-loops skill: injects the unchecked items of the project's "Open loops" list.
# List: the open GitHub issue labelled open-loops; without a repo ~/.claude/open-loops/<folder>.md.
# Silent when there is no list or nothing is open. Skill: ~/.claude/skills/open-loops/SKILL.md
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
dir="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$dir" 2>/dev/null || exit 0

GH_JSON=""
if command -v gh >/dev/null && git remote get-url origin >/dev/null 2>&1; then
  GH_JSON="$(gh issue list --label open-loops --state open --json number,title,body,url --limit 5 2>/dev/null)"
fi
export GH_JSON LOOPS_FILE="$HOME/.claude/open-loops/$(basename "$dir").md"

exec python3 - <<'EOF'
import json, os, re, sys
source = body = None
try:
    issues = json.loads(os.environ.get("GH_JSON") or "[]")
except ValueError:
    issues = []
if issues:
    d = min(issues, key=lambda x: x["number"])
    source, body = "#%s %s" % (d["number"], d["url"]), d["body"]
elif os.path.exists(os.environ["LOOPS_FILE"]):
    source, body = os.environ["LOOPS_FILE"], open(os.environ["LOOPS_FILE"], encoding="utf-8").read()
if not source:
    sys.exit(0)
items, heading = [], ""
for line in body.splitlines():
    if line.startswith("### "):
        heading = line[4:].strip()
    m = re.match(r"\s*- \[ \] (.*)", line)
    if m:
        items.append("- (%s) %s" % (heading, m.group(1)))
if not items:
    sys.exit(0)
text = ("Open loops (%d unchecked, %s) — open-loops skill. End your first answer with a one-line reminder in the "
        "user's language; check off items you resolve:\n" % (len(items), source)) + "\n".join(items)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}, ensure_ascii=False))
EOF
