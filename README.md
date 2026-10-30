# acik-konular — Claude Code için açık uç takibi

Bir konuyu konuşurken başka konuya atlayınca geride kalanlar unutuluyor: cevaplanmamış sorular, Claude'un bulduğu ama
düzeltilmemiş hatalar, onay bekleyen öneriler. Issue açmayı hatırlamak da kullanıcıya kalınca açılmıyor.

Bu beceri yakalama işini Claude'a verir:

- Konu değişince geride açık uç kaldıysa Claude **sormadan** projenin tek "Açık konular" listesine yazar
  (GitHub'da `acik-konu` etiketli tek issue; depo yoksa `~/.claude/acik-konular/<klasör>.md`).
- Her oturum açılışında SessionStart kancası açık maddeleri Claude'a verir; Claude ilk cevabında tek satırla hatırlatır.
- Çözülen madde işaretlenir, sonucu yazılır.

## Kurulum

```bash
git clone https://github.com/mkilicer/claude-acik-konular
mkdir -p ~/.claude/skills ~/.claude/scripts
cp -r claude-acik-konular/skills/acik-konular ~/.claude/skills/
cp claude-acik-konular/hooks/acik_konular_hook.sh ~/.claude/scripts/ && chmod +x ~/.claude/scripts/acik_konular_hook.sh
```

`~/.claude/settings.json` içine kanca:

```json
"hooks": {
  "SessionStart": [
    { "hooks": [ { "type": "command", "command": "~/.claude/scripts/acik_konular_hook.sh", "timeout": 15 } ] }
  ]
}
```

Becerinin kendiliğinden devreye girmesi için `~/.claude/CLAUDE.md`'ye bir satır:

```markdown
- Kullanıcı konu değiştirince geride kalan cevapsız soruyu, bulduğun hatayı ya da onay bekleyen önerini sormadan
  projenin "Açık konular" listesine yaz (`acik-konular` becerisi).
```

Gerekenler: `gh` (giriş yapılmış), `python3`.

---

## English summary

**Open-loop tracking for Claude Code.** When a conversation jumps to a new topic, unanswered questions, bugs Claude found
but didn't fix, and proposals awaiting approval get lost — and nobody remembers to open an issue. This skill makes
capturing them Claude's job: on topic change Claude appends them (without asking) to a single per-project
"open topics" list (one GitHub issue labelled `acik-konu`, or a local markdown file when there is no repo). A
SessionStart hook feeds the unchecked items back at the start of every session so Claude reminds the user in one line.
The skill text is in Turkish; the mechanism is language-agnostic.
