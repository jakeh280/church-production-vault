---
title: Maintenance Scripts
type: meta
tags: [meta, reference]
updated: 2026-08-16
status: active
source: template, distilled from CLAUDE.md
---
# Maintenance Scripts

Deterministic helpers in `scripts/` that enforce the house rules. Run them from the vault root. They are pure Python with no dependencies and no LLM involved, which is the point: a cheap automated pass can just run them and report, and a human can trust the output without re-reading every page.

**Fixers** default to read-only **check** mode (exit 1 when fixes are pending), add `--apply` to write, then review `git diff`. **Reporters and guards** are read-only: they surface state (`pii_guard` also blocks commits) but never edit content.

---

## Fixers (`--apply` to write)

| Script | What it checks and fixes | Check | Apply |
|--------|--------------------------|-------|-------|
| `reflow.py` | Hard-wrapped prose paragraphs → joins each into one continuous line (leaves tables, lists, code, and two-space hard breaks alone; reflows callout bodies too) | `python3 scripts/reflow.py` | `python3 scripts/reflow.py --apply` |
| `fm_fix.py` | Frontmatter values with `[[wikilinks]]` or `colon: space` that break Obsidian's YAML parser → quotes them | `python3 scripts/fm_fix.py` | `python3 scripts/fm_fix.py --apply` |

---

## Reporters & guards (read-only)

| Script | What it reports | Run |
|--------|-----------------|-----|
| `link_check.py` | Unresolved `[[wikilinks]]` in page **bodies**, alias-aware, base-aware, `inbox/` excluded, with close-match suggestions. Exits 1 if any are found. | `python3 scripts/link_check.py` |
| `staleness.py` | Operational pages never verified (blank `verified:`) or verified more than N months ago (`--months N`, default 6). Exits 1 if any. | `python3 scripts/staleness.py` |
| `health.py` | Flat JSON of vault health metrics, page count, source and verified coverage, open questions, unresolved links, orphans. Always exits 0. Add `--record` to append the day's metrics to `wiki/00-Meta/health-history.jsonl` (idempotent per day) and print the trend delta. | `python3 scripts/health.py [--record]` |
| `bring_up.py` | The tickler: scans page bodies for actionable keywords (due, balance, renew, expire, EOL, warranty, deadline) on a line carrying a parseable date, and buckets them OVERDUE / ≤30 days / ≤horizon. Read-only, exits 0. | `python3 scripts/bring_up.py [--days N]` |
| `pii_guard.py` | Secret and PII scanner for the pre-commit gate, flags credential **values**, SSNs, keys, tokens, and salary figures. Descriptive prose like "passwords stripped" is ignored; suppress a false positive on a line with `pii-guard-ok`. `--all` scans the whole vault; `--install-hook` wires up the pre-commit hook. Exit 1 blocks the commit. | `python3 scripts/pii_guard.py` |

---

## The pre-commit guard

`scripts/git-hooks/pre-commit` is tracked in the repo, but git hooks are local config and are **not** cloned. Wire it up once per machine:

```bash
python3 scripts/pii_guard.py --install-hook
```

It does two things on every commit: scans staged text for secret-shaped values, and **blocks any staged binary outright**. That second rule matters more than it looks, `pii_guard` is a text scanner and cannot see inside a PDF, PNG, or spreadsheet, so a binary would sail past the secret check entirely. Binaries belong in `inbox/` (gitignored) or in their native system.

Genuine exception, used deliberately and rarely: `git commit --no-verify`.

---

## Conventions for adding scripts

Check by default. Idempotent and conservative, never delete content, never invent facts. Reversible, with git as the backstop. Keep them dependency-free so they run on a fresh machine with nothing installed but Python 3.
