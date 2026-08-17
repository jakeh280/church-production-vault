# Church Production Vault

**Everything you know about your church's production system stops living in your head.**

Take photos of your rack. Drop in a manual, a quote, your meeting notes. Tell an AI agent to ingest it, and get back a structured, cross-linked wiki that answers questions six months later, with citations, and with an honest distinction between what someone confirmed and what the AI guessed.

It's a folder of Markdown files. No app, no account, no server, no subscription. Free, MIT licensed, from [Overflow Creative](https://overflowcreative.net).

---

## Start here

You don't need to know how any of this works. You need an AI coding agent that can run commands in a folder on your computer, Claude Code, Codex, Gemini CLI, or Cursor. Open a terminal, go to wherever you keep your stuff (`cd ~/Documents`), start the agent there, and paste this:

> Set up a Church Production Vault for me in a new folder called `my-church-vault`, using the template at https://github.com/jakeh280/church-production-vault
>
> Clone it into that folder, replace the template's git history with a fresh one of my own, then run `python3 scripts/pii_guard.py --install-hook` inside it. After that, read `CLAUDE.md` in that folder and run the first-run setup interview on me, one topic at a time.

That's the whole install. The agent does the setup, then interviews you for about ten minutes about your church, your room, your team, and how work actually gets approved. It fills in the config, deletes the example content, writes your first real pages, and logs day one.

**Then use it.** Walk out to your rack and take ten photos: the front of the rack, the back of it, the patch panel, the labels, the console, whatever's confusing. Drop them in `inbox/`, and say:

> ingest

That's the loop, and it's the fastest way to get a room documented. The agent reads what's actually legible in the photos, writes the pages, and flags what it couldn't read clearly instead of guessing at a model number. Same loop for a PDF manual, a vendor quote, or your notes from a Tuesday meeting.

**Worth doing, either now or later:** open the folder in [Obsidian](https://obsidian.md) as a vault. Everything works without it, but Obsidian is what makes the links clickable, the callouts render, and the database views show up as sortable, filterable tables. Bases need Obsidian 1.9.10 or newer.

**One more, when you're ready:** the setup above lives only on your laptop, which means a dead laptop takes it with it. Pushing it to a **private** GitHub repo is the backup, and it's how the rest of your team gets a copy. Ask the agent to walk you through it. Private, always. Nothing about a production vault belongs in a public repo.

---

## Why this exists

Church production knowledge lives in three places: one person's head, a spreadsheet nobody updates, and a group chat from eight months ago. Mostly the head. When that person is out sick, the room doesn't run right. When they leave, it walks out with them, and the next person rebuilds it by trial and error on a Sunday morning.

That is the actual problem this solves. Not note-taking. Getting the system out of one person's head and into something the whole team can query.

The usual fix is "write documentation," and it usually fails, because documentation goes stale silently, and a wiki nobody trusts is worse than no wiki. So this template is built around the two questions that actually determine whether a page is worth acting on:

- **Where did this come from?** (`source:`): a person on a date, an ingested manual, a photo you took, or `agent-inferred`, which is the lowest trust level and is marked as such
- **Did a human confirm it against reality, and when?** (`verified:`), and **only a human ever sets this.** An AI can write a page; it cannot verify one

Blank is an honest answer. A page that says "nobody has checked this" is more useful than a page that quietly implies someone did.

The rest of the design follows from one rule: **every fact lives in exactly one place, and every other page links to it.** Two pages that both state the gain structure are two pages that will disagree the day one gets updated.

---

## What it does

**Ingest**: you drop source material in `inbox/`, photos, manuals, quotes, meeting notes. The agent reads it, tells you what it found before writing anything, updates the pages it affects (rather than creating a fifth page about the same console), updates the index, logs the action, and archives or deletes the original depending on what's in it.

**Answer**: you ask a question. It answers from your pages with citations, not from general knowledge about church audio. When the vault doesn't know, it says so and creates the stub. Every unanswered question becomes the backlog for what to document next.

**Lint**: periodically, it checks itself: contradictions between pages, the same value typed in two places, claims with no source, pages overdue for re-verification, orphans, and counts hardcoded into prose that will silently go stale.

---

## What's in the folder

```
CLAUDE.md              The operating card. Every rule the agent follows
AGENTS.md              Pointer to CLAUDE.md, so non-Claude tools find it too
inbox/                 Drop source material here. Gitignored, never synced
wiki/                  00-Meta, 01-Production (gear, assets, purchases,
                       procedures, signal flow, troubleshooting), 02-Events,
                       03-Creative, 04-Vendors, 05-Reference, 06-Meetings,
                       07-Canvas, 08-Bases, 09-Templates, 10-Log
scripts/               Seven maintenance scripts + a pre-commit secret guard
.claude/skills/        setup, ingest, lint
```

**Five database views** in `08-Bases/`, driven entirely by frontmatter: a gear register with a needs-attention triage view, a spend and service log, an open-questions queue, a verification dashboard, and the daily log.

**Seven maintenance scripts**, pure Python, no dependencies. They fix hard-wrapped prose and broken frontmatter, report unresolved links, flag pages overdue for re-verification, surface upcoming renewal and warranty dates, and scan for secrets before you commit.

---

## What never goes in this vault

Read this before you put anything in. It's a hard boundary, not a guideline, and a church vault will be tempted by every item on the list.

- **Personnel or HR files**: reviews, discipline, hiring notes, volunteer performance or attendance records
- **Pastoral care or counseling notes**: anything shared in confidence, ever
- **Giving, donor, and offering records** of any kind
- **Staff salary or compensation information**, and anything out of payroll
- **Any personal congregation member data**: names attached to circumstances, prayer requests, contact lists
- **Live credentials**: passwords, keys, tokens, door codes, Wi-Fi keys. A page may say *where* a credential lives; it must never hold the value

**Equipment spend is a different thing and it belongs here.** What a console cost, what a repair was quoted at, which vendor invoiced it, when a service agreement renews: that is equipment history, and it is what the spend register is for. The line is the subject, not the dollar sign.

This is written into `CLAUDE.md`, so the agent enforces it during ingest: sensitive source files get distilled into a safe page and then **deleted**, not archived. `scripts/pii_guard.py` backstops the credential half at commit time, and `inbox/` is gitignored, so nothing you drop in it is ever synced anywhere.

---

## Design notes, if you're curious

**Plain Markdown, deliberately.** No database, no runtime, no service to keep alive. It works offline, in any editor, with any model, in five years. The ceiling is lower than a real app; the floor is far higher.

**Derived state is never typed by hand.** Which pages have open questions, which need verification, how many of something you own. All of it computed from frontmatter by a Base, so nobody maintains a second copy and nothing drifts.

**Live documents are pointers, not copies.** The patch sheet that changes every week gets a page saying what it is and where it lives, never a frozen snapshot that goes wrong within a month. Those pages are marked `live_doc: true` and excluded from verification, because there's nothing there to go stale.

**Logs are append-only.** `10-Log/` is one file per day of what actually happened. Git holds the structural history; the logs hold the narrative. Between them you can reconstruct why something is the way it is, which is the question that actually comes up.

**The agent is told what it may not decide.** It never sets `verified:`. It escalates sensitivity judgments. It asks before structural changes.

---

## Making it yours

`CLAUDE.md` is the whole system. Edit it freely: it's a document of rules in plain English, not code, and the agent follows whatever it says. Add folders, add types, add tags, change the conventions. Easiest way is to just tell the agent what you want changed and have it make the edit.

Two things to be careful with:

- `Log.base` filters on a hardcoded folder path. If you renumber or rename `10-Log`, update that filter in the same edit. A stale filter fails silently and just shows an empty table. The other four Bases filter on frontmatter, so they survive any reorganization.
- If you add a rule, add it to `CLAUDE.md` rather than telling the agent in chat. Chat is forgotten; the file travels.

---

## What it won't do

This is a memory aid, not an operator. It does not replace training, and it does not replace knowing your room. A page can be wrong. A page can be confidently, fluently wrong, which is worse. That's exactly why `verified:` exists and why only a human sets it. The vault is designed to tell you what it hasn't checked.

Use it to stop re-deriving the same answer every six months. Don't use it to hand someone a runbook for a room they've never stood in.

---

## Credits

Built by [Jake Hill](https://overflowcreative.net), a church Production Director running this system on a real production vault daily. Extracted and generalized so other teams don't have to invent it.

Issues and pull requests welcome. If you adapt it for your room and something in the structure fought you, that's worth an issue. The friction you hit is the next version.

MIT licensed. Do whatever you want with it.
