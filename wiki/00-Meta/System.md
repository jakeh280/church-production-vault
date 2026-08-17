---
title: System Dossier
type: meta
tags: [meta]
updated: 2026-08-16
status: active
source: template
---
# System Dossier

**This page is the vault's memory of itself.** Domain facts (gear, rooms, procedures, vendors) live on their own wiki pages. *This* page holds how the vault and the agent work: architecture, integrations, decisions about the system, and what's still open.

The split matters because it's the SSOT rule applied to scope. A gear page that starts describing how the agent connects to a spreadsheet has leaked system detail into content, move it here and leave a one-line pointer.

> [!info] Starting state
> This is a fresh vault. Everything below is a placeholder shape for you to fill in as decisions get made. Delete what never becomes true.

---

## 1. Where we are

Fresh install. Fill this in after the first month with an honest read on what the vault is actually being used for versus what it was set up for.

---

## 2. Trust model

Two independent axes, both defined in full in `CLAUDE.md`:

- **Provenance** (`source:`): where a claim came from at all. Ranges from a named human on a date, to an ingested document, down to `agent-inferred`, which is the lowest trust level and should be visibly marked.
- **Verification** (`verified:`): whether a human confirmed the page against physical reality, and when. Only a human sets this. Blank is an honest answer, not a failure.

A page can be well-sourced and unverified (someone wrote it down, nobody has checked the rack). It can also be verified and thinly sourced. Track both.

---

## 3. Architecture

**Current shape:** a plain folder of Markdown, read and written by an AI agent, versioned in git, viewed in Obsidian.

That's deliberately unambitious, and it's the whole trick. The vault has no runtime, no database, and no service to keep alive. It works the same on a laptop with no network, in any editor, with any model, in five years.

Record here as they get decided:

- Which machines hold a copy, and how they stay in sync
- Which agent tools operate in this vault
- Any connectors or integrations, and what each is allowed to read or write
- Any scheduled or automated passes

---

## 4. Storage, sync & backup

- **Git**: structural history. Private remote only, if any. See `CLAUDE.md` → Git for the confidentiality boundary.
- **`inbox/`**: local staging only, never synced. Gitignored.
- **Binaries**: never in the repo. They live in `inbox/` or in their native system (shared drive, vendor portal, email).

Record the actual backup situation here once it exists. "It's in git on one laptop" is not a backup; write down the truth either way.

---

## 5. Human-in-the-loop approval gate

Decide and record where the agent may act alone and where it must ask. A reasonable starting line:

- **Alone:** reading, answering, drafting, mechanical lint fixes, log appends, index rows
- **Ask first:** creating or changing facts on a page, structural moves and renames, deleting anything, any judgment about sensitivity
- **Never:** setting `verified:`, writing anything from the "What Never Goes in This Vault" list

---

## 6. Integrations backlog

Systems that could eventually feed the vault, and the connect-versus-wall-off decision for each. Be explicit about the wall-offs. A system deliberately left out is a decision worth recording, not an oversight to rediscover later.

The default posture for anything holding personal data (church management software, giving platforms, HR systems) is **wall off**. If a connection ever makes sense, it reads a narrow, depersonalized slice and nothing else.

---

## 7. Open work

### Documentation tracks

What's actively being documented right now, and what's deliberately deferred.

### Demand-driven documentation

The direction this vault takes by default: **document what gets asked about.** Every question the vault can't answer is a gap, and a logged gap is the backlog. Don't try to document the whole building up front. It's a large amount of work with no signal about what matters, and most of it goes stale before anyone reads it.

### Open confirmations

Never hand-list these. See [[Open-Confirmations]]. It derives them from frontmatter.

---

## 8. Format & structure decisions

### Why Obsidian-flavored Markdown

Wikilinks, callouts, and Bases give a plain-text vault the ergonomics of a database without a database. Every file stays readable in any editor if Obsidian ever goes away.

### Anti-bloat: controlled decomposition, not file sprawl

A new page must earn its existence. Prefer a new **section** on the page that already owns the subject. Split a subsystem into its own page only when it is genuinely large and standalone, and then the source page keeps a summary plus a link, never both the summary and the detail.

The failure mode this prevents: a vault of 400 thin pages where every fact is in two of them.

### Meta audience boundary

`00-Meta/` is for people building and maintaining the *vault*. The rest of `wiki/` is for people running *production*. When a page starts explaining the vault's own machinery to an operator who just wants to know how to start the console, that content belongs here instead.

---

## 9. Roadmap

Where this could go, tiered by effort. Keep it honest. An aspirational roadmap nobody revisits is just a mood.
