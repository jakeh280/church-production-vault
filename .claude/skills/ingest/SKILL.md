---
name: ingest
description: Absorb source material from inbox/ into the wiki, photos of a rack or gear, manuals, quotes, meeting notes. Read it, discuss the takeaways, write or update pages, update the index, log the action, and archive or purge the original. Use whenever the user drops a file or photo in inbox/ or says "ingest this".
---

# Ingest

The core loop of this vault. Source material goes in, structured pages come out, and the original is dealt with.

## Before you start

If `CLAUDE.md` still contains `<<UNFILLED>>`, stop and run the setup interview first. Ingesting into an unconfigured vault produces pages with no owner and no context.

## Steps

### 1. Read the source

Read everything in `inbox/` that hasn't been processed, or the specific file the user named. Read it fully before writing anything.

If it's a binary you can't read (a PDF you can't open, a proprietary format), say so plainly rather than guessing at its contents from the filename.

**Photos are first-class source material.** A phone photo of a rack, a patch panel, a fixture label, a console screen, or a serial-number sticker is often the fastest way to get a room documented. Read what is actually legible in the image and nothing more. A label you can half-read is not a model number; a rack unit you recognize by shape is not a confirmed make. Write only what you can literally see, and put everything else in a `[!question]` callout with `open_questions: true` so the user can walk back out and check. Photos are exactly where a confident guess does the most damage, because the guess reads like it came off a nameplate. When several photos cover one rack or one room, ingest them together and describe the layout top to bottom, rather than making a page per photo.

### 2. Screen it for sensitivity: before anything else

Check the source against **What Never Goes in This Vault** in `CLAUDE.md`. If it contains credentials, personnel notes, giving records, or congregation member data:

- Ingest **only** the safe, depersonalized distillate
- **Delete the original**: do not move it to `_processed/`
- Log the purge explicitly in today's log file

On *any* doubt, ask the user before proceeding. This is the one step where being wrong is expensive.

### 3. Discuss the takeaways

Before writing, tell the user what you found and what you propose to do with it, which pages you'll create, which you'll update, what's ambiguous. This is where they catch a misread, and it costs one message.

Flag anything the source states only loosely. Convert relative dates to absolute anchors now ("last spring" → "~spring 2025"), while the context is still in front of you.

### 4. Write

Prefer **extending an existing page** over creating a new one. A new page has to earn its existence; a new section on the owning page usually serves better.

For each page you touch:
- Full frontmatter, `title`, `type`, `tags`, `updated`, `status`, `source`
- `source:` names where this actually came from: the inbox path, a person and date, a URL. If you inferred something, say `agent-inferred` and mark the claim inline with `[!question]`, then set `open_questions: true`
- Leave `verified:` **blank** on operational pages. You did not confirm anything against reality; a human does that
- Append below a `### Updated YYYY-MM-DD` heading rather than rewriting existing content
- Scan for facts that belong to another page and link to them instead of copying, see the SSOT rule in `CLAUDE.md`

If the source names equipment worth tracking individually, create `type: gear-asset` pages in `01-Production/Gear-Assets/`. If it's a purchase, repair, or service call, create a `type: gear-event` page in `01-Production/Gear-Events/`.

### 5. Update the index

Add or update the row in `wiki/index.md`, page name, one-line summary, type tag. A page that isn't in the index is invisible to future queries.

### 6. Log it

Append a bullet to `wiki/10-Log/<today>.md`, creating the file with `type: log` frontmatter if it's the first entry of the day. Append only, never rewrite a log file.

Format: `- **ingest**, <what came in, what it changed>` with `[[wikilinks]]` to the affected pages.

### 7. Deal with the original

Move it to `inbox/_processed/`, or delete it if step 2 flagged it as sensitive.

### 8. Close the loop

Run `python3 scripts/link_check.py` to catch wikilinks you introduced that don't resolve yet. Then commit:

```bash
git add wiki/ && git commit -m "ingest: <short description>"
```

## Before you finish: the synthesis pass

Look across the vault, not just at what you touched. Anything worth surfacing unprompted? Vendor concentration, a renewal date approaching, deferred maintenance clustering on one system, a fact that now contradicts a page you didn't edit. This is where the vault earns its keep. A filing cabinet doesn't do it.
