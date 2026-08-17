# Church Production Vault

**An AI-readable knowledge base for church production teams.** Drop a manual, a quote, or your meeting notes into a folder, tell an AI agent to ingest it, and get back a structured, cross-linked wiki that answers questions six months later, with citations, and with an honest distinction between what someone confirmed and what the AI guessed.

It's a folder of Markdown files. No app, no account, no server, no subscription. It works in Obsidian, in any text editor, with Claude Code, Codex, Gemini, Cursor, or a chat window with the folder attached.

Free, MIT licensed, from [Overflow Creative](https://overflowcreative.net).

---

## Why this exists

Church production knowledge lives in three places: one person's head, a spreadsheet nobody updates, and a group chat from eight months ago. When that person is out, the room doesn't run. When they leave, it's gone.

The usual fix is "write documentation," and it usually fails, because documentation goes stale silently, and a wiki nobody trusts is worse than no wiki. So this template is built around the two questions that actually determine whether a page is worth acting on:

- **Where did this come from?** (`source:`): a person on a date, an ingested manual, or `agent-inferred`, which is the lowest trust level and is marked as such
- **Did a human confirm it against reality, and when?** (`verified:`), and **only a human ever sets this.** An AI can write a page; it cannot verify one

Blank is an honest answer. A page that says "nobody has checked this" is more useful than a page that quietly implies someone did.

The rest of the design follows from one rule: **every fact lives in exactly one place, and every other page links to it.** Two pages that both state the gain structure are two pages that will disagree the day one gets updated.

---

## What you get

```
CLAUDE.md              The operating card. Every rule the agent follows
AGENTS.md              Pointer to CLAUDE.md, so non-Claude tools find it too
inbox/                 Drop source material here. Gitignored, never synced
wiki/
  00-Meta/             How the vault works, schemas, conventions, system notes
  01-Production/       Gear, gear assets, purchases & repairs, procedures,
                       signal flow, troubleshooting, reference
  02-Events/           Christmas, Easter, camps, conferences
  03-Creative/         Series and projects production supports
  04-Vendors/          Integrators, rental houses, repair shops
  05-Reference/        Background material that isn't a live procedure
  06-Meetings/         One file per meeting, YYYY-MM-DD-Short-Title.md
  07-Canvas/           Signal flow and rack diagrams
  08-Bases/            Database views, derived, never hand-maintained
  09-Templates/        Page shapes to copy
  10-Log/              One append-only file per day
scripts/               Seven maintenance scripts + a pre-commit secret guard
.claude/skills/        setup, ingest, lint
```

**Five database views** built into `08-Bases/`, driven entirely by frontmatter. A gear register with a needs-attention triage view, a spend and service log, an open-questions queue, a verification dashboard, and the daily log.

**Seven maintenance scripts**, pure Python, no dependencies. They fix hard-wrapped prose and broken frontmatter, report unresolved links, flag pages overdue for re-verification, surface upcoming renewal and warranty dates, and scan for secrets before you commit.

---

## Getting started

**1. Get the folder.**

```bash
git clone https://github.com/OWNER/church-production-vault.git my-church-vault
cd my-church-vault
rm -rf .git && git init
```

That last line is deliberate. You want your own history, not this repo's.

**2. Install the secret guard.** One time, on each machine:

```bash
python3 scripts/pii_guard.py --install-hook
```

**3. Open it with an AI agent** in the folder (Claude Code, Codex, Gemini CLI, Cursor, or a chat window with the folder attached) and say:

> Set up this vault.

It reads the first-run block in `CLAUDE.md`, interviews you for about ten minutes about your church, your room, your team, and your systems, fills in the config, deletes the example content, writes your first real pages, and logs day one.

**4. Use it.** Drop something in `inbox/` and say `ingest`. That's the loop.

**Optional: open the folder in Obsidian** as a vault. Everything works without it, but Obsidian is what makes the links clickable, the callouts render, and the `.base` files show up as sortable, filterable tables. **Bases need Obsidian 1.9.10 or newer**; 1.10+ is recommended.

---

## The three things it does

**Ingest**: you drop source material in `inbox/`. The agent reads it, tells you what it found before writing anything, updates the pages it affects (rather than creating a fifth page about the same console), updates the index, logs the action, and archives or deletes the original depending on what's in it.

**Answer**: you ask a question. It answers from your pages with citations, not from general knowledge about church audio. When the vault doesn't know, it says so and creates the stub. Every unanswered question becomes the backlog for what to document next.

**Lint**: periodically, it checks itself: contradictions between pages, the same value typed in two places, claims with no source, pages overdue for re-verification, orphans, and counts hardcoded into prose that will silently go stale.

---

## What never goes in this vault

Read this before you put anything in. It's a hard boundary, not a guideline, and a church vault will be tempted by every item on the list.

- **Personnel or HR files**: reviews, discipline, hiring notes, volunteer performance or attendance records
- **Pastoral care or counseling notes**: anything shared in confidence, ever
- **Financial records, giving, or donor information**
- **Staff salary or compensation information**
- **Any personal congregation member data**: names attached to circumstances, prayer requests, contact lists
- **Live credentials**: passwords, keys, tokens, door codes, Wi-Fi keys. A page may say *where* a credential lives; it must never hold the value

This is written into `CLAUDE.md`, so the agent enforces it during ingest: sensitive source files get distilled into a safe page and then **deleted**, not archived. `scripts/pii_guard.py` backstops the credential half at commit time.

**If you sync this to GitHub, make the repo private.** Nothing about a production vault belongs in a public one. `inbox/` is gitignored and binaries are blocked at commit, because a text scanner cannot see inside a PDF.

---

## Design notes, if you're curious

**Plain Markdown, deliberately.** No database, no runtime, no service to keep alive. It works offline, in any editor, with any model, in five years. The ceiling is lower than a real app; the floor is far higher.

**Derived state is never typed by hand.** Which pages have open questions, which need verification, how many of something you own. All of it computed from frontmatter by a Base. Nobody maintains a second copy, so nothing drifts.

**Live documents are pointers, not copies.** The patch sheet that changes every week gets a page saying what it is and where it lives. Never a frozen snapshot that goes wrong within a month. Those pages are marked `live_doc: true` and excluded from verification, because there's nothing there to go stale.

**Logs are append-only.** `10-Log/` is one file per day of what actually happened. Git holds the structural history; the logs hold the narrative. Between them you can reconstruct why something is the way it is, which is the question that actually comes up.

**The agent is told what it may not decide.** It never sets `verified:`. It escalates sensitivity judgments. It asks before structural changes. Those limits are in `CLAUDE.md`, in plain language, and you can change them. It's your vault.

---

## Making it yours

`CLAUDE.md` is the whole system. Edit it freely: it's a document of rules in plain English, not code, and the agent follows whatever it says. Add folders, add types, add tags, change the conventions.

Two things to be careful with:

- `Verification-Dashboard.base` and `Log.base` filter on hardcoded folder paths. If you renumber or rename a folder, update those filters in the same edit. A stale filter fails silently and just shows an empty table.
- If you add a rule, add it to `CLAUDE.md` rather than telling the agent in chat. Chat is forgotten; the file travels.

---

## A caveat worth stating plainly

This is a memory aid, not an operator. It does not replace training, and it does not replace knowing your room. A page can be wrong. A page can be confidently, fluently wrong, which is worse. That's exactly why `verified:` exists and why only a human sets it. The vault is designed to tell you what it hasn't checked.

Use it to stop re-deriving the same answer every six months. Don't use it to hand someone a runbook for a room they've never stood in.

---

## Credits

Built by [Jake Hill](https://overflowcreative.net), Production Director at a two-service church, running this system on a real production vault daily. Extracted and generalized so other teams don't have to invent it.

Issues and pull requests welcome. If you adapt it for your room and something in the structure fought you, that's worth an issue. The friction you hit is the next version.

MIT licensed. Do whatever you want with it.
