---
name: open-loops
description: Captures open loops — unanswered questions, bugs you found but did not fix, proposals waiting for the user's decision — into one per-project "Open loops" list, checks them off when resolved, and reminds the user at session start. Use WITHOUT ASKING whenever the user moves to a new topic and something from the previous one is left open. Also use when the user asks what is still open / pending / forgotten, in any language (e.g. "what's left", "open items", "açık konular", "neler kaldı", "offene Punkte", "pendientes", "en suspens"), or when an item gets resolved.
---

# Open loops

People jump between topics. When they do, the loose ends of the previous topic — a question you asked that was never
answered, a bug you spotted on the side, a proposal waiting for a yes/no — scroll away and are forgotten. Remembering
to open an issue is exactly the step that gets skipped. This skill makes capturing them **your** job, not the user's.

## Language

Write list items, headings and reminders in **the language the user is using with you**. The mechanism (label, file
path, checkbox syntax) is fixed; the words are not. Numbers, file paths, commands and identifiers stay verbatim.

## Where the list lives

Exactly one list per project:

1. **GitHub repo** (`gh repo view` works): a single open issue labelled `open-loops`.
   Find it: `gh issue list --label open-loops --state open --json number,title,body,url`.
   None yet → create the label if missing (`gh label create open-loops --color fbca04 --description "Open loops: unanswered questions, found bugs, pending decisions"`)
   and the issue, titled "Open loops" in the user's language (e.g. "Açık konular", "Offene Punkte").
   More than one open → use the oldest and tell the user.
2. **No GitHub repo:** `~/.claude/open-loops/<project-folder-name>.md` (outside the repo). Same format.

Body format — `###` section headings, checkbox items:

```markdown
### Waiting for a decision
- [ ] **Short name.** What is proposed, with the numbers behind it (measurement, date). Decision needed: <what the user must decide>
### Problems found
- [ ] **Short name.** What happened, where (file:line / log time), impact. Decision needed: <fix? how?>
### Unanswered questions
- [ ] **Short name.** Who asked, what exactly.
### For the record (no decision needed)
- A measurement or answer worth keeping; no checkbox.
```

Each item must stand alone: someone who never saw the conversation (including you in a new session) must understand
what is pending. Add the date. Never invent numbers; if you did not measure it, say so.

## When to write — without asking

- The user switched topics and the previous one left any of: a question of yours with no answer, a bug or
  inconsistency you found and did not fix, a proposal awaiting approval, a "let's look at it later".
- A long answer ends with several decisions for the user — record them after answering.
- The user says "add it to the list", "don't let us forget", or similar.

Do not ask first: the list lives in the user's own repo or home folder, edits are reversible, and the user delegated this
job to you. Edit with `gh issue edit <n> --body-file <file>` (read the body first with `gh issue view <n> --json body`,
add the item, keep everything else). If the item is already on the list, update it instead of adding a duplicate.

Do not write: work you are about to finish in this session; anything the user explicitly dropped (if it is on the
list, close it).

## Closing items

- When resolved (decided, fixed, answered): turn `[ ]` into `[x]` and append `→ <outcome, date>`. The reasoning behind a
  decision still belongs in the commit message / code comment / docs; the list only tracks.
- Once everything is checked, delete the checked items to keep the body short. Do not close the issue when it is
  empty — the next open loop goes there.

## Reminding

- At session start the hook `~/.claude/scripts/open_loops_hook.sh` (SessionStart) injects the unchecked items. If there are
  any, end your first answer with one line, e.g. `Open loops: 3 (#65) — oldest: <short name>`. If the user is busy with
  something else, do not elaborate.
- If your answer resolves an item on the list, say so at the end and check it off.
- If the user asks what is open, list it briefly: one line per item, with the decision needed.

## Telling the user

When you add an item, end your answer with one line: `Added to open loops: <short name> (#<issue>)`, in the user's
language. Give the link the first time.
