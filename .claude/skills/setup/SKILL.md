---
name: setup
description: First-run interview for a new Church Production Vault. Asks about the church, the room, the team, and the systems, then fills in CLAUDE.md, writes the team structure page, clears the example content, and logs day one. Run this once, before any other work in a fresh vault.
---

# Setup: first-run interview

You are setting up a fresh copy of the Church Production Vault for a new user. Nothing in this vault is theirs yet: `CLAUDE.md` has an unfilled config block, and `wiki/` contains example pages about a fictional church.

Your job is to turn this into *their* vault in one conversation, and to end with them having actually used it once.

## How to run the interview

**Conversational, not a form.** Ask one topic at a time and react to the answers. If they say something that makes a later question irrelevant, skip it. If an answer opens a door worth walking through ("we just replaced the console"), note it. That's the first real ingest.

**Everything is skippable.** If they don't know or don't care, write `not yet documented` and move on. A half-filled config is fine; a stalled setup is not. You can always fill gaps later.

**Do not guess.** If they don't tell you a name, a model number, or a schedule, it does not go in the vault. This is the provenance rule from `CLAUDE.md`, and it starts now.

**Keep it short.** Aim for under ten minutes of their time. Everything below is one message's worth of questions per block, not one question per line.

---

## Block 1: The church

- Church name, and the town or city
- One or two campuses, or more? Which one does this vault cover?
- Weekend service schedule, how many services, what times, what day(s)
- Any midweek programming this vault should know about (youth, kids, prayer, rehearsals)
- Roughly how many people attend, if they want to say, useful for sizing recommendations, entirely optional

## Block 2: Them

- Their name and title
- Who they report to (title is enough; a name is fine if they offer it)
- Are they full-time staff, part-time, or a volunteer running production
- How long have they been in the role, helps you calibrate how much you explain

## Block 3: The team

- Who else is on the production team, paid or volunteer, and roughly what each person covers
- How many volunteers serve on a typical weekend, and on what rotation
- Who else touches production gear that isn't on the team (worship leader, kids director, facilities)

> Write this into `wiki/00-Meta/Team-Structure.md`. **Roles and reporting lines only.** No performance notes, no attendance records, no phone numbers, no personal detail. If they start telling you a volunteer is unreliable, do not write it down. Say plainly that personnel notes stay out of the vault, and keep going.

## Block 4: The rooms and the rig

- Which rooms does this vault cover, main auditorium, youth room, kids room, lobby, portable setup
- For the main room: what's the audio console, the video setup (cameras, switcher, or none), the lighting console, the presentation software, the streaming platform
- Anything portable, rented, or shared between rooms
- Is there a project underway right now. An install, an upgrade, something broken they're chasing

Don't try to build the whole gear register in the interview. You want enough to create three or four real starting pages and to know what the room *is*. The rest arrives through `inbox/` over time.

## Block 5: How work actually happens

- How does someone request production support, a form, an email, a project tool, a hallway conversation
- How do purchases get approved, is there a budget, a purchase order, an executive who signs off? Who is the first approver?
- Which systems stay authoritative and should never be copied into this vault (scheduling software, the patch sheet spreadsheet, the shared drive, the ticketing tool)

> That last one matters more than it sounds. Anything that changes weekly becomes a **pointer page** (`live_doc: true`) that says what it is and where it lives, not a frozen copy that silently goes stale.

## Block 6: Ground rules

Read them the short version of **What Never Goes in This Vault** from `CLAUDE.md` and confirm they're good with it. Then ask:

- Will this vault be synced to a git remote? If yes, tell them it must be a **private** repo, and walk them through `python3 scripts/pii_guard.py --install-hook`.
- Will anyone else read or edit it, or is it just them?

---

## What to write when the interview is done

Do these in order. Tell the user what you're doing as you go.

1. **Fill the Setup Config block in `CLAUDE.md`.** Replace every `<<UNFILLED>>` with the real answer or `not yet documented`. Do not leave the marker text anywhere in the file.

2. **Write `wiki/00-Meta/Team-Structure.md`** from Block 3: roles and reporting lines, `type: meta`, `source: setup interview (<date>)`.

3. **Delete the example content.** Every page listed under "Example content" in `wiki/index.md` is fictional and must go, leaving it in place is how a fake vendor ends up in a real purchase conversation later. Delete the files, then rewrite `wiki/index.md` as a real index of what now exists.

4. **Create their first real pages** (three or four) from Blocks 4 and 5, using the templates in `wiki/09-Templates/`. Good first pages: one `gear` page for the main audio system, one `gear` page for the video or presentation system, one `procedure` stub for weekend service startup, and one `live_doc: true` pointer for whatever spreadsheet or tool they named in Block 5. Leave `verified:` **blank** on all of them. Nobody has confirmed anything against reality yet, and that's the honest state.

5. **Write today's log file** at `wiki/10-Log/<today>.md` with a bullet recording that the vault was set up.

6. **Run the checks**, `python3 scripts/health.py` and `python3 scripts/link_check.py`, and fix anything they surface.

7. **Commit**, if the vault is a git repo: `git add wiki/ CLAUDE.md && git commit -m "setup: initialize vault for <church>"`.

---

## Land the ending

Do not finish with a summary of what you wrote. Finish by getting them to use it, with one concrete next action:

> Walk out to the booth and take ten photos: the front of the rack, the back of it, the patch panel, the labels, the console. Drop them in `inbox/` and tell me to ingest. That's the whole loop, and photos are the fastest way to get a room documented, no typing required.

Photos are the best default first ingest because they cost the user nothing but a walk. A manual, a quote, or the last meeting's notes work just as well if they'd rather start at a desk.

If they already mentioned a current project in Block 4, name *that* specifically instead. "You said the lighting console upgrade is in progress, drop the quote in `inbox/` and I'll start the page" beats a generic invitation every time.

---

## If the vault is already set up

If `CLAUDE.md` has no `<<UNFILLED>>` markers, this vault is configured. Don't re-run the interview. Say so, and offer the narrower thing instead: updating one config value, re-running the team structure page, or auditing what's still missing.
