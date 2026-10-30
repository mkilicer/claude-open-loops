#!/bin/bash
# SessionStart kancası: projenin "Açık konular" listesindeki işaretlenmemiş maddeleri bağlama koyar.
# Liste: GitHub'da acik-konu etiketli açık issue; depo yoksa ~/.claude/acik-konular/<klasör>.md.
# Sessiz çalışır: liste yoksa ya da boşsa hiçbir şey yazmaz. Beceri: ~/.claude/skills/acik-konular/SKILL.md
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
dizin="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$dizin" 2>/dev/null || exit 0

GH_JSON=""
if command -v gh >/dev/null && git remote get-url origin >/dev/null 2>&1; then
  GH_JSON="$(gh issue list --label acik-konu --state open --json number,title,body,url --limit 5 2>/dev/null)"
fi
export GH_JSON DOSYA="$HOME/.claude/acik-konular/$(basename "$dizin").md"

exec python3 - <<'EOF'
import json, os, re, sys
kaynak = govde = None
try:
    issues = json.loads(os.environ.get("GH_JSON") or "[]")
except ValueError:
    issues = []
if issues:
    d = min(issues, key=lambda x: x["number"])
    kaynak, govde = "#%s %s" % (d["number"], d["url"]), d["body"]
elif os.path.exists(os.environ["DOSYA"]):
    kaynak, govde = os.environ["DOSYA"], open(os.environ["DOSYA"], encoding="utf-8").read()
if not kaynak:
    sys.exit(0)
acik, baslik = [], ""
for s in govde.splitlines():
    if s.startswith("### "):
        baslik = s[4:].strip()
    m = re.match(r"\s*- \[ \] (.*)", s)
    if m:
        acik.append("- (%s) %s" % (baslik, m.group(1)))
if not acik:
    sys.exit(0)
metin = ("Açık konular (%d madde, %s) — acik-konular becerisi. İlk cevabının sonunda tek satırla hatırlat; "
         "çözülen maddeyi işaretle:\n" % (len(acik), kaynak)) + "\n".join(acik)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": metin}}, ensure_ascii=False))
EOF
