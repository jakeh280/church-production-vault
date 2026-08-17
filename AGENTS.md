# AGENTS.md

**This file intentionally holds no rules of its own.** The authoritative instructions for this vault live in [`CLAUDE.md`](CLAUDE.md), read it in full and follow it exactly. It is the single source of truth for your role, the three-layer structure, the frontmatter / verification / provenance conventions, the Single-Source-of-Truth rule, the linking and embedding rules, the ingest, query, and lint workflows, the inbox-file lifecycle, and what must never be stored here.

Any agent operating in this folder, Claude Code, Codex, Gemini, Cursor, or a chat window with the folder attached, should treat `CLAUDE.md` as its system instructions. If `CLAUDE.md` and this file ever appear to disagree, `CLAUDE.md` wins. Do not duplicate its content here; update `CLAUDE.md` instead so every tool stays in sync.

**First run:** if the Setup Config block at the top of `CLAUDE.md` still reads `<<UNFILLED>>`, run the setup interview in `.claude/skills/setup/SKILL.md` before doing anything else.
