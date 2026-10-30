# open-loops — a Claude Code skill that never lets a loose end drop

You ask Claude something, the conversation jumps to another topic, and the loose ends of the first one are gone:
the question Claude asked that you never answered, the bug it spotted on the side, the proposal still waiting for
your yes/no. Opening an issue for them is exactly the step everyone forgets.

**open-loops makes capturing them Claude's job, not yours.**

- When you switch topics and something is left open, Claude adds it — without asking — to **one list per project**:
  a single GitHub issue labelled `open-loops`, or `~/.claude/open-loops/<folder>.md` when there is no repo.
- A **SessionStart hook** feeds the unchecked items back at the start of every session; Claude reminds you in one line.
- Resolved items are checked off with their outcome.
- **Multilingual:** items and reminders are written in whatever language you talk to Claude in. The mechanism
  (label, file path, checkboxes) is language-independent, and the skill triggers on "what's left?" in any language
  ("neler kaldı", "offene Punkte", "pendientes", "en suspens"…).

## Install

```bash
git clone https://github.com/mkilicer/claude-open-loops
mkdir -p ~/.claude/skills ~/.claude/scripts
cp -r claude-open-loops/skills/open-loops ~/.claude/skills/
cp claude-open-loops/hooks/open_loops_hook.sh ~/.claude/scripts/ && chmod +x ~/.claude/scripts/open_loops_hook.sh
```

Add the hook to `~/.claude/settings.json`:

```json
"hooks": {
  "SessionStart": [
    { "hooks": [ { "type": "command", "command": "~/.claude/scripts/open_loops_hook.sh", "timeout": 15 } ] }
  ]
}
```

So the skill fires on its own when topics change, add one line to `~/.claude/CLAUDE.md`:

```markdown
- When I change topics, add any unanswered question, bug you found or proposal awaiting my decision to the project's
  open-loops list without asking (`open-loops` skill).
```

Requires `gh` (logged in) and `python3`.

## Why

Built after a long trading-bot session where several findings and pending decisions silently disappeared behind
new questions. Existing options (TodoWrite, task-management, session-handoff) all depend on the user remembering to
trigger them — which is the very thing that fails.
